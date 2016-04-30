import matplotlib.pyplot as plt
import os.path
import re
from PIL import Image
from PIL import ImageColor
from skimage.filters import threshold_otsu
from skimage.util import img_as_ubyte
from wordcloud import WordCloud
import numpy as np
import colorsys

class Visualizer:
    def __init__(self,User,stringToCloud,customImage,customStopWords,bgColor="white",textColor="multi",keyBoardImage=None,includeOtherInfo=False,includeKeyBoard=False):
        self.User = User
        self.stringToCloud = stringToCloud
        self.customImage = customImage
        self.customStopWords = customStopWords
        self.bgColor = bgColor
        self.textColor = textColor
        self.keyBoardImage = keyBoardImage
        self.includeOtherInfo = includeOtherInfo
        self.includeKeyBoard = includeKeyBoard
        pass

    def get_single_color_func(self,color):
        """Create a color function which returns a single hue and saturation with.
        different values (HSV). Accepted values are color strings as usable by PIL/Pillow.
        >>> color_func1 = get_single_color_func('deepskyblue')
        >>> color_func2 = get_single_color_func('#00b4d2')
        """
        old_r, old_g, old_b = ImageColor.getrgb(color)
        rgb_max = 255.
        h, s, v = colorsys.rgb_to_hsv(old_r / rgb_max, old_g / rgb_max, old_b / rgb_max)

        def single_color_func(word=None, font_size=None, position=None,
                              orientation=None, font_path=None, random_state=None):
            """Random color generation.
            Additional coloring method. It picks a random value with hue and
            saturation based on the color given to the generating function.
            Parameters
            ----------
            word, font_size, position, orientation  : ignored.
            random_state : random.Random object or None, (default=None)
              If a random object is given, this is used for generating random numbers.
            """
            if random_state is None:
                random_state = Random()
            r, g, b = colorsys.hsv_to_rgb(h, s, v)#random_state.uniform(0.2, 1))
            return 'rgb({:.0f}, {:.0f}, {:.0f})'.format(r * rgb_max, g * rgb_max, b * rgb_max)
        return single_color_func

    def fig2img(self, fig):
        """
        @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
        @param fig a matplotlib figure
        @return a Python Imaging Library ( PIL ) image
        """
        # put the figure pixmap into a numpy array

        # draw the renderer
        fig.canvas.draw()
 
        # Get the RGBA buffer from the figure
        w,h = fig.canvas.get_width_height()
        buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
        buf.shape = (w, h,4)
 
        # canvas.tostring_argb give pixmap in ARGB mode.  Roll the ALPHA
        # channel to have it in RGBA mode
        buf = np.roll(buf, 3, axis = 2)
        
        w, h, d = buf.shape
        return Image.frombytes("RGBA", (w ,h), buf.tostring())
        #return Image.fromstring("RGBA", (w ,h), buf.tostring())

    def makecloud(self, hcmask, mostfavourite, mostretweeted, input,output):
        wordcloud = None
        if self.textColor == "multi":
            wordcloud = WordCloud(background_color=self.bgColor, mask=hcmask, stopwords=self.customStopWords, relative_scaling = 0.3) 
        else:
            wordcloud = WordCloud(background_color=self.bgColor, mask=hcmask, stopwords=self.customStopWords, relative_scaling = 0.3,color_func=self.get_single_color_func(self.textColor)) 
        wordcloud.generate(self.stringToCloud)

        if self.includeOtherInfo:
            plt.figure()
            plt.imshow(wordcloud)
            plt.tick_params(axis='both',which='both',bottom='off',top='off',left='off', right ='off',labelleft='off',labelbottom='off')
    
            def format(str1):
                if len(str1) > 70:
                    ind = str1[:71][::-1].index(' ')
                    return str1[:70 - ind] + '\n' + str1[70 - ind:]
                else:
                    return str1
    
            if (mostretweeted.id == mostfavourite.id):
                label = "Most RE(" + str(mostretweeted.shares) + ") Most Favs(" + str(mostfavourite.likes) + "):\n" + format(mostfavourite.statusText)
                plt.xlabel(label)
            else:
                label = "Most RE(" + str(mostretweeted.shares) + "):" + format(mostretweeted.statusText) + "\nMost Favs(" + str(mostfavourite.likes) + "):" + format(mostfavourite.statusText)
                plt.xlabel(label)
            label = self.User.twitterName + '\n' + '@' + self.User.twitterId + '\nFollowers:' + str(self.User.twitterFollower)
            plt.ylabel(label,labelpad=70).set_rotation(0)
            fig = plt.gcf()
            fig.set_size_inches(12, 10.5)
            if self.includeKeyBoard and self.keyBoardImage != None:
                img = self.fig2img(fig)
                (w1,h1) = img.size
                (w2,h2) = self.keyBoardImage.size
                result = Image.new('RGB', (w1, h1 + h2))
                result.paste(im=img, box=(0, 0))
                result.paste(im=self.keyBoardImage, box=(0, h1))
                result.save(output)
            else:
                fig.savefig(output, dpi = 200)
        else:
            wordcloud.to_file(output)

    def makecloudForFile(self,mostfavourite,mostretweeted,input,output,invert):
        img = Image.open(input)
        img = img.convert('L')
        img = img.resize((980,1080), Image.ANTIALIAS)
        hcmask = np.array(img)
        hcmask[hcmask < 150] = 0
        hcmask[hcmask >= 150] = 255
        self.makecloud(hcmask, mostfavourite, mostretweeted, input,output)
        img.close()

    def makeImageForThresh(self, input, thresh, invert):
        img = self.customImage 
        imgb = img_as_ubyte(img)
        binary = imgb > thresh
        if invert:
            for i in range(len(binary)):
                for j in range(len(binary[i])):
                    binary[i][j] = not binary[i][j]
        plt.figure()
        plt.imshow(binary,cmap=plt.cm.gray)
        plt.tick_params(axis='both',which='both',bottom='off',top='off',left='off', right ='off',labelleft='off',labelbottom='off')
        plt.axis('off')
        fig = plt.gcf()
        #print(os.getcwd())
        fig.savefig(input, dpi=200,bbox_inches='tight')

    def makeCloudFor(self,mostfavourite, mostretweeted, thresh,suffix,invert=False):
        input = 'rawImages\\' + self.User.twitterId + suffix
        output = 'outputImages\\' + self.User.twitterId + suffix
        try:
            if not os.path.isfile(input) and thresh > -1:
                self.makeImageForThresh(input,thresh,invert)
            if os.path.isfile(input) and not os.path.isfile(output):
                self.makecloudForFile(mostfavourite,mostretweeted,input,output,invert)
            return output
        except:
            pass

    def getFirstTweetWithoutMention(self,liTweet):
        for tweet in liTweet:
            if re.search('@[^\s]+',tweet.statusText) is None:
                return tweet
        pass

    def Visualize(self):
        img = self.customImage 
        self.customImage = img.convert('L')
        img = img.convert('L')
        thresh = threshold_otsu(img_as_ubyte(img))
        img = img.resize((980,1080), Image.ANTIALIAS)

        # compute famous ones
        tweets = [x for x in self.User.statuses if x.statusType == 1]
        mostfavourite = self.getFirstTweetWithoutMention(sorted(tweets,key = lambda p:p.likes,reverse=True))
        mostretweeted = self.getFirstTweetWithoutMention(sorted(tweets,key = lambda p:p.shares,reverse=True))

        output = []
        output.append(self.makeCloudFor(mostfavourite, mostretweeted, thresh,'_1.jpg'))
        output.append(self.makeCloudFor(mostfavourite, mostretweeted, (thresh + 0) // 2,'_2.jpg'))
        output.append(self.makeCloudFor(mostfavourite, mostretweeted, (thresh + 255) // 2,'_3.jpg'))
        output.append(self.makeCloudFor(mostfavourite, mostretweeted, thresh,'_4.jpg',invert = True))
        output.append(self.makeCloudFor(mostfavourite, mostretweeted, (thresh + 0) // 2,'_5.jpg',invert = True))
        output.append(self.makeCloudFor(mostfavourite, mostretweeted, (thresh + 255) // 2,'_6.jpg',invert = True))

        plt.close('all')
        return output
