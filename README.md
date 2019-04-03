# DeOldify

Image [<img src="https://colab.research.google.com/assets/colab-badge.svg" align="center">](https://colab.research.google.com/github/jantic/DeOldify/blob/master/ImageColorizerColab.ipynb)  |  Video [<img src="https://colab.research.google.com/assets/colab-badge.svg" align="center">](https://colab.research.google.com/github/jantic/DeOldify/blob/master/VideoColorizerColab.ipynb) 

[Get more updates on Twitter <img src="result_images/Twitter_Social_Icon_Rounded_Square_Color.svg" width="16">](https://twitter.com/citnaj)


Simply put, the mission of this project is to colorize and restore old images and film footage.  I'll get into the details in a bit, but first let's see some pretty pictures and videos! 

-----------------------

### Example Images

Maria Anderson as the Fairy Fleur de farine and Lyubov Rabtsova as her page in the ballet “Sleeping Beauty” at the Imperial Theater, St. Petersburg, Russia, 1890.

![Ballerinas](result_images/Ballerinas.jpg)

Woman relaxing in her livingroom (1920, Sweden)

![SwedenLivingRoom](result_images/SweedishLivingRoom1920.jpg)

Medical Students pose with a cadaver around 1890

![MedStudents](result_images/MedStudentsCards.jpg)

Surfer in Hawaii, 1890

![1890Surfer](result_images/1890Surfer.jpg)

Whirling Horse, 1898

![WhirlingHorse](result_images/WhirlingHorse.jpg)

Interior of Miller and Shoemaker Soda Fountain, 1899

![SodaFountain](result_images/SodaShop.jpg)

Paris in the 1880s

![Paris1880s](result_images/Paris1880s.jpg)

Edinburgh from the sky in the 1920s

![Edinburgh](result_images/FlyingOverEdinburgh.jpg)

Texas Woman in 1938

![TexasWoman](result_images/TexasWoman.jpg)

People watching a television set for the first time at Waterloo station, London, 1936

![Television](result_images/FirstTV1930s.jpg)

Geography Lessons in 1850

![Geography](result_images/GeographyLessons.jpg)

Chinese Opium Smokers in 1880

![OpiumReal](result_images/ChineseOpium1880s.jpg)


#### Note that even really old and/or poor quality photos will still turn out looking pretty cool:

Deadwood, South Dakota, 1877

![Deadwood](result_images/OldWest.jpg)

Siblings in 1877

![Deadwood](result_images/Olds1875.jpg)

Portsmouth Square in San Franscisco, 1851

![PortsmouthSquare](result_images/SanFran1850sRetry.jpg)

Samurais, circa 1860s

![Samurais](result_images/Samurais.jpg)

#### Granted, the model isn't always perfect.  This one's red hand drives me nuts because it's otherwise fantastic:

Seneca Native in 1908

![Samurais](result_images/SenecaNative1908.jpg)

#### It can also colorize b&w line drawings:

![OpiumDrawing](result_images/OpiumSmokersDrawing.jpg)

-----------------------

### The Technical Details

This is a deep learning based model.  More specifically, what I've done is combined the following approaches:

#### **Self-Attention Generative Adversarial Network** (https://arxiv.org/abs/1805.08318)  
Except the generator is a **pretrained U-Net**, and I've just modified it to have the spectral normalization and self-attention.  It's a pretty straightforward translation.

#### **Two Time-Scale Update Rule** (https://arxiv.org/abs/1706.08500)
This is also very straightforward – it's just one to one generator/critic iterations and higher critic learning rate. This is modified to incorporate a "threshold" critic loss that makes sure that the critic is "caught up" before moving on to generator training.  This is particularly useful for the "NoGAN" method described below.

#### **NoGAN**
There's no paper here! This is a new type of GAN training that I've developed to solve some key problems in the previous DeOldify model. The gist is that you get the benefits of GAN training while spending minimal time doing direct GAN training.  More details are at the bottom of the readme (it's a doozy).

#### **Generator Loss**
Loss during NoGAN learning is two parts:  One is a basic Perceptual Loss (or Feature Loss) based on VGG16 – this just biases the generator model to replicate the input image.  The second is the loss score from the critic.  For the curious – Perceptual Loss isn't sufficient by itself to produce good results.  It tends to just encourage a bunch of brown/green/blue – you know, cheating to the test, basically, which neural networks are really good at doing!  Key thing to realize here is that GANs essentially are learning the loss function for you – which is really one big step closer to toward the ideal that we're shooting for in machine learning.  And of course you generally get much better results when you get the machine to learn something you were previously hand coding.  That's certainly the case here.

**Of note:**  There's no longer any "Progressive Growing of GANs" type training going on here.  It's just not needed in lieu of the superior results obtained by the "NoGAN" technique described above.

The beauty of this model is that it should be generally useful for all sorts of image modification, and it should do it quite well.  What you're seeing above are the results of the colorization model, but that's just one component in a pipeline that I'm developing with the exact same approach.

-----------------------

### This Project, Going Forward
So that's the gist of this project – I'm looking to make old photos and film look reeeeaaally good with GANs, and more importantly, make the project *useful*.  In the meantime though this is going to be my baby and I'll be actively updating and improving the code over the foreseeable future.  I'll try to make this as user-friendly as possible, but I'm sure there's going to be hiccups along the way.  

Oh and I swear I'll document the code properly...eventually.  Admittedly I'm *one of those* people who believes in "self documenting code" (LOL).

-----------------------

### Getting Started Yourself- Easiest Approach
The easiest way to get started is to go straight to the Colab notebooks: 

Image [<img src="https://colab.research.google.com/assets/colab-badge.svg" align="center">](https://colab.research.google.com/github/jantic/DeOldify/blob/master/ImageColorizerColab.ipynb) | Video [<img src="https://colab.research.google.com/assets/colab-badge.svg" align="center">](https://colab.research.google.com/github/jantic/DeOldify/blob/master/VideoColorizerColab.ipynb) 

Special thanks to Matt Robinson and María Benavente for their image Colab notebook contributions, and Robert Bell for the video Colab notebook work!

-----------------------

### Getting Started Yourself- Your Own Machine (not -as- easy)

#### Hardware and Operating System Requirements

* **(Training Only) BEEFY Graphics card**.  I'd really like to have more memory than the 11 GB in my GeForce 1080TI (11GB).  You'll have a tough time with less.  The Generators and Critic are ridiculously large.  
* **(Colorization Alone) A decent graphics card**. Approximately 4GB+ memory video cards should be sufficient.
* **Linux (or maybe Windows 10)**  I'm using Ubuntu 16.04, but nothing about this precludes Windows 10 support as far as I know.  I just haven't tested it and am not going to make it a priority for now.  

#### Easy Install

You should now be able to do a simple install with Anaconda. Here are the steps:

Open the command line and navigate to the root folder you wish to install.  Then type the following commands 
```console
git clone https://github.com/jantic/DeOldify.git DeOldify
cd DeOldify
conda env create -f environment.yml
```
Then start running with these commands:
```console
source activate deoldify
jupyter lab
```

From there you can start running the notebooks in Jupyter Lab, via the url they provide you in the console.  


--------------------------
#### Installation Details

This project is built around the wonderful Fast.AI library.  Prereqs, in summary:
* **Fast.AI 1.0.46** (and its dependencies)
* **Jupyter Lab** `conda install -c conda-forge jupyterlab`
* **Tensorboard** (i.e. install Tensorflow) and **TensorboardX** (https://github.com/lanpa/tensorboardX).  I guess you don't *have* to but man, life is so much better with it.  FastAI now comes with built in support for this- you just  need to install the prereqs: `conda install -c anaconda tensorflow-gpu` and `pip install tensorboardX`
* **ImageNet** – Only if you're training, of course. It has proven to be a great dataset for my purposes.  http://www.image-net.org/download-images

--------------------------
#### Pretrained Weights 

To start right away on your own machine with your own images or videos without training the models yourself, you'll need to download the generator weights and drop them in the /models/ folder.

[Download 'artistic' model weights here](https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth?dl=0)

[Download 'stable' model weights here](https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth?dl=0)

[Download 'video' model weights here](https://www.dropbox.com/s/336vn9y4qwyg9yz/ColorizeVideo_gen.pth?dl=0)


You can then do image colorization in this notebook:  [ImageColorizer.ipynb](ImageColorizer.ipynb) 

And you can do video colorization in this notebook:  [VideoColorizer.ipynb](VideoColorizer.ipynb) 

The notebooks should be able to guide you from here.

A more complete list of available pretrained weights, including those for critics, can be found at the bottom of the readme.

-------------------------
### Stuff That Should Probably Be In A Paper

#### **How to Achieve Stable Video**

NoGAN training is crucial to getting the kind of stable and colorful images seen in this iteration of DeOldify. NoGAN training combines the benefits of GAN training (wonderful colorization) while eliminating the nasty side effects (like flickering objects in video). Believe it or not, video is rendered using isolated image generation without any sort of temporal modeling tacked on. The process performs 30-60 minutes of the GAN portion of "NoGAN" training, using 1% to 3% of imagenet data once.  Then, as with still image colorization, we "DeOldify" individual frames before rebuilding the video.

In addition to improved video stability, there is an interesting thing going on here worth mentioning. It turns out the models I run, even different ones and with different training structures, keep arriving at more or less the same solution.  That's even the case for the colorization of things you may think would be arbitrary and unknowable, like the color of clothing, cars, and even special effects (as seen in "Metropolis").  My best guess is that the models are learning some interesting rules about how to colorize based on subtle cues present in the black and white images that I certainly wouldn't expect to exist.  This result leads to nicely deterministic and consistent results, and that means you don't have track model colorization decisions because they're not arbitrary.  Additionally, they seem remarkably robust so that even in moving scenes the renders are very consistent.

Other ways to stabilize video add up as well. First, generally speaking rendering at a higher resolution (higher render_factor) will increase stability of colorization decisions.  This stands to reason because the model has higher fidelity image information to work with and will have a greater chance of making the "right" decision consistently.  Closely related to this is the use of resnet101 instead of resnet34 as the backbone of the generator- objects are detected more consistently and corrrectly with this. This is especially important for getting good, consistent skin rendering.  It can be particularly visually jarring if you wind up with "zombie limbs", for example.

Additionally, gaussian noise augmentation during training appears to help but at this point the conclusions as to just how much are bit more tenuous (I just haven't formally measured this yet).  This is loosely based on work done in style transfer video, described here:  https://medium.com/element-ai-research-lab/stabilizing-neural-style-transfer-for-video-62675e203e42.  

Special thanks go to Rani Horev for his contributions in implementing this noise augmentation.

-------------------------
#### **What is NoGAN???**

This is a new type of GAN training that I've developed to solve some key problems in the previous DeOldify model. It provides the benefits of GAN training while spending minimal time doing direct GAN training.  Instead, most of the training time is spent pretraining the generator and critic separately with more straight-forward, fast and reliable conventional methods.  A key insight here is that those more "conventional" methods generally get you most of the results you need, and that GANs can be used to close the gap on realism. During the very short amount of actual GAN training the generator not only gets the full realistic colorization capabilities that used to take days of progressively resized GAN training, but it also doesn't accrue nearly as much of the artifacts and other ugly baggage of GANs. In fact, you can pretty much eliminate glitches and artifacts almost entirely depending on your approach. As far as I know this is a new technique. And it's incredibly effective. 

The steps are as follows: First train the generator in a conventional way by itself with just the feature loss. Next, generate images from that, and train the critic on distinguishing between those outputs and real images as a basic binary classifier. Finally, train the generator and critic together in a GAN setting (starting right at the target size of 192px in this case).  Now for the weird part:  All the useful GAN training here only takes place within a very small window of time.  There's an inflection point where it appears the critic has transferred everything it can that is useful to the generator. Past this point, image quality oscillates between the best that you can get at the inflection point, or bad in a predictable way (orangish skin, overly red lips, etc).  There appears to be no productive training after the inflection point.  And this point lies within training on just 1% to 3% of the Imagenet Data!  That amounts to about 30-60 minutes of training at 192px.  

The hard part is finding this inflection point.  So far, I've accomplished this by making a whole bunch of model save checkpoints (every 0.1% of data iterated on) and then just looking for the point where images look great before they go totally bonkers with orange skin (always the first thing to go). Additionally, generator rendering starts immediately getting glitchy and inconsistent at this point, which is no good particularly for video. What I'd really like to figure out is what the tell-tale sign of the inflection point is that can be easily automated as an early stopping point.  Unfortunately, nothing definitive is jumping out at me yet.  For one, it's happening in the middle of training loss decreasing- not when it flattens out, which would seem more reasonable on the surface.   

Another key thing about NoGAN training is you can repeat pretraining the critic on generated images after the initial GAN training, then repeat the GAN training itself in the same fashion.  This is how I was able to get extra colorful results with the "artistic" model.  But this does come at a cost currently- the output of the generator becomes increasingly inconsistent and you have to experiment with render resolution (render_factor) to get the best result.  But the renders are still glitch free and way more consistent than I was ever able to achieve with the original DeOldify model. You can do about five of these repeat cycles, give or take, before you get diminishing returns, as far as I can tell.  

Keep in mind- I haven't been entirely rigorous in figuring out what all is going on in NoGAN- I'll save that for a paper. That means there's a good chance I'm wrong about something.  But I think it's definitely worth putting out there now because I'm finding it very useful- it's solving basically much of my remaining problems I had in DeOldify.

This builds upon a technique developed in collaboration with Jeremy Howard and Sylvain Gugger for Fast.AI's Lesson 7 in version 3 of Practical Deep Learning for Coders Part I. The particular lesson notebook can be found here: https://github.com/fastai/course-v3/blob/master/nbs/dl1/lesson7-superres-gan.ipynb  

-------------------------
### Weights, Weights, and More Weights


#### Completed Generator Weights

[artistic](https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth?dl=0)
[stable](https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth?dl=0)
[video](https://www.dropbox.com/s/336vn9y4qwyg9yz/ColorizeVideo_gen.pth?dl=0)

#### Completed Critic Weights

[artistic](https://www.dropbox.com/s/8g5txfzt2fw8mf5/ColorizeArtistic_crit.pth?dl=0)
[stable](https://www.dropbox.com/s/7a8u20e7xdu1dtd/ColorizeStable_crit.pth?dl=0)
[video](https://www.dropbox.com/s/0401djgo1dfxdzt/ColorizeVideo_crit.pth?dl=0)

#### Pretrain Only Generator Weights

[artistic](https://www.dropbox.com/s/9zexurvrve141n9/ColorizeArtistic_PretrainOnly_gen.pth?dl=0)
[stable](https://www.dropbox.com/s/mdnuo1563bb8nh4/ColorizeStable_PretrainOnly_gen.pth?dl=0)
[video](https://www.dropbox.com/s/avzixh1ujf86e8x/ColorizeVideo_PretrainOnly_gen.pth?dl=0)

#### Pretrain Only Critic Weights

[artistic](https://www.dropbox.com/s/lakxe8akzjgjnmh/ColorizeArtistic_PretrainOnly_crit.pth?dl=0)
[stable](https://www.dropbox.com/s/b3wka56iyv1fvdc/ColorizeStable_PretrainOnly_crit.pth?dl=0)
[video](https://www.dropbox.com/s/j7og84cbhpa94gs/ColorizeVideo_PretrainOnly_crit.pth?dl=0)

-------------------------
### Want More?

I'll be posting more results on Twitter. [<img src="result_images/Twitter_Social_Icon_Rounded_Square_Color.svg" width="28">](https://twitter.com/citnaj)
