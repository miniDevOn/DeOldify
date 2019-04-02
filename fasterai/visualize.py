from fastai.core import *
from fastai.vision import *
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .filters import IFilter, MasterFilter, ColorizerFilter
from .generators import gen_inference_deep, gen_inference_wide
from IPython.display import display
from tensorboardX import SummaryWriter
from scipy import misc
from PIL import Image 
import ffmpeg
import youtube_dl
import gc


class ModelImageVisualizer():
    def __init__(self, filter:IFilter, results_dir:str=None):
        self.filter = filter
        self.results_dir=None if results_dir is None else Path(results_dir)
    
    def _clean_mem(self):
        return
        #torch.cuda.empty_cache()
        #gc.collect()

    def _open_pil_image(self, path:Path)->Image:
        return PIL.Image.open(path).convert('RGB')

    def plot_transformed_image(self, path:str, figsize:(int,int)=(20,20), render_factor:int=None)->Image:
        path = Path(path)
        result = self.get_transformed_image(path, render_factor)
        orig = self._open_pil_image(path)
        fig,axes = plt.subplots(1, 2, figsize=figsize)
        self._plot_image(orig, axes=axes[0], figsize=figsize)
        self._plot_image(result, axes=axes[1], figsize=figsize)

        if self.results_dir is not None:
            self._save_result_image(path, result)

    def _save_result_image(self, source_path:Path, image:Image):
        result_path = self.results_dir/source_path.name
        image.save(result_path)

    def get_transformed_image(self, path:Path, render_factor:int=None)->Image:
        self._clean_mem()
        orig_image = self._open_pil_image(path)
        filtered_image = self.filter.filter(orig_image, orig_image, render_factor=render_factor)
        return filtered_image

    def _plot_image(self, image:Image, axes:Axes=None, figsize=(20,20)):
        if axes is None: 
            _,axes = plt.subplots(figsize=figsize)
        axes.imshow(np.asarray(image)/255)
        axes.axis('off')

    def _get_num_rows_columns(self, num_images:int, max_columns:int)->(int,int):
        columns = min(num_images, max_columns)
        rows = num_images//columns
        rows = rows if rows * columns == num_images else rows + 1
        return rows, columns

class VideoColorizer():
    def __init__(self, vis:ModelImageVisualizer):
        self.vis=vis
        workfolder = Path('./video')
        self.source_folder = workfolder/"source"
        self.bwframes_root = workfolder/"bwframes"
        self.audio_root = workfolder/"audio"
        self.colorframes_root = workfolder/"colorframes"
        self.result_folder = workfolder/"result"

    def _purge_images(self, dir):
        for f in os.listdir(dir):
            if re.search('.*?\.jpg', f):
                os.remove(os.path.join(dir, f))

    def _get_fps(self, source_path: Path)->float:
        probe = ffmpeg.probe(str(source_path))
        stream_data = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        avg_frame_rate = stream_data['avg_frame_rate']
        fps_num=avg_frame_rate.split("/")[0]
        fps_den = avg_frame_rate.rsplit("/")[1]
        return round(float(fps_num)/float(fps_den))

    def _download_video_from_url(self, source_url, source_path:Path):
        if source_path.exists(): source_path.unlink()

        ydl_opts = {    
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',     
            'outtmpl': str(source_path)   
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([source_url])

    def _extract_raw_frames(self, source_path:Path):
        bwframes_folder = self.bwframes_root/(source_path.stem)
        bwframe_path_template = str(bwframes_folder/'%5d.jpg')
        bwframes_folder.mkdir(parents=True, exist_ok=True)
        self._purge_images(bwframes_folder)
        ffmpeg.input(str(source_path)).output(str(bwframe_path_template), format='image2', vcodec='mjpeg', qscale=0).run(capture_stdout=True)


    def _colorize_raw_frames(self, source_path:Path):
        colorframes_folder = self.colorframes_root/(source_path.stem)
        colorframes_folder.mkdir(parents=True, exist_ok=True)
        self._purge_images(colorframes_folder)
        bwframes_folder = self.bwframes_root/(source_path.stem)

        for img in progress_bar(os.listdir(str(bwframes_folder))):
            img_path = bwframes_folder/img
            if os.path.isfile(str(img_path)):
                color_image = self.vis.get_transformed_image(str(img_path))
                color_image.save(str(colorframes_folder/img))
    
    def _build_video(self, source_path:Path):
        result_path = self.result_folder/source_path.name
        colorframes_folder = self.colorframes_root/(source_path.stem)
        colorframes_path_template = str(colorframes_folder/'%5d.jpg')
        result_path.parent.mkdir(parents=True, exist_ok=True)
        if result_path.exists(): result_path.unlink()
        fps = self._get_fps(source_path)

        ffmpeg.input(str(colorframes_path_template), format='image2', vcodec='mjpeg', framerate=str(fps)) \
            .output(str(result_path), crf=17, vcodec='libx264') \
            .run(capture_stdout=True)
        
        print('Video created here: ' + str(result_path))

    def colorize_from_url(self, source_url, file_name:str):    
        source_path =  self.source_folder/file_name
        self._download_video_from_url(source_url, source_path)
        self._colorize_from_path(source_path)

    def colorize_from_file_name(self, file_name:str):
        source_path =  self.source_folder/file_name
        self._colorize_from_path(source_path)

    def _colorize_from_path(self, source_path:Path):
        self._extract_raw_frames(source_path)
        self._colorize_raw_frames(source_path)
        self._build_video(source_path)


def get_video_colorizer(render_factor:int=36)->VideoColorizer:
    return get_stable_video_colorizer(render_factor=render_factor)

def get_stable_video_colorizer(root_folder:Path=Path('./'), weights_name:str='ColorizeImagesStable_gen', 
        results_dir='result_images', render_factor:int=36)->VideoColorizer:
    learn = gen_inference_wide(root_folder=root_folder, weights_name=weights_name)
    filtr = MasterFilter([ColorizerFilter(learn=learn)], render_factor=render_factor)
    vis = ModelImageVisualizer(filtr, results_dir=results_dir)
    return VideoColorizer(vis)


def get_image_colorizer(render_factor:int=36, artistic:bool=False)->ModelImageVisualizer:
    if artistic:
        return get_artistic_image_colorizer(render_factor=render_factor)
    else:
        return get_stable_image_colorizer(render_factor=render_factor)

def get_stable_image_colorizer(root_folder:Path=Path('./'), weights_name:str='ColorizeImagesStable_gen', 
        results_dir='result_images', render_factor:int=36)->ModelImageVisualizer:
    learn = gen_inference_wide(root_folder=root_folder, weights_name=weights_name)
    filtr = MasterFilter([ColorizerFilter(learn=learn)], render_factor=render_factor)
    vis = ModelImageVisualizer(filtr, results_dir=results_dir)
    return vis

def get_artistic_image_colorizer(root_folder:Path=Path('./'), weights_name:str='ColorizeImagesArtistic_gen', 
        results_dir='result_images', render_factor:int=36)->ModelImageVisualizer:
    learn = gen_inference_deep(root_folder=root_folder, weights_name=weights_name)
    filtr = MasterFilter([ColorizerFilter(learn=learn)], render_factor=render_factor)
    vis = ModelImageVisualizer(filtr, results_dir=results_dir)
    return vis




