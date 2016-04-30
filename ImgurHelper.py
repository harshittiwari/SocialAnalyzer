from imgurpython import ImgurClient
import Config

#{'deletehash': 'pOb9UqTvfI0wOxU', 'id': 'gNNNC'}
#True
def CreateAlbumAndUploadImages(albumName,albumDescription,images):
    access_token,refresh_token,client_id,client_secret = Config.getImgurKeys()
    client = ImgurClient(client_id, client_secret)
    client.set_user_auth(access_token,refresh_token)
    fields = {}
    fields['title'] = albumName
    fields['description'] = albumDescription
    fields['privacy'] = 'public'
    x = client.create_album(fields)
    y = client.album_add_images(x['id'],images)
    return x

def UploadPhotoInAlbum(id,album):
    access_token,refresh_token,client_id,client_secret = Config.getImgurKeys()
    client = ImgurClient(client_id, client_secret)
    client.set_user_auth(access_token,refresh_token)
    config = {
		'name':  'htht!',
		'title': 'hththt!',
		'description': 'this is a test'}   
    return client.album_add_images(album,[id])

def UploadPhoto(image,title,name,description):
    access_token,refresh_token,client_id,client_secret = Config.getImgurKeys()
    client = ImgurClient(client_id, client_secret)
    client.set_user_auth(access_token,refresh_token)
    config = {
		'name':  title,
		'title': name,
		'description': description}    
    retVal = None
    tryCount = 0
    while tryCount < 4:
        try:
            retVal = client.upload_from_path(image, config=config, anon=False)
            break
        except:
            tryCount += 1
    if retVal == None:
        retVal = client.upload_from_path(image, config=config, anon=False)
    return retVal

#def main():
#    #x = CreateAlbum('Album 101','Album 101 desciption')
#    id = []
#    id.append( UploadPhoto('outputImages\\narendramodi_6.jpg')['id'])
#    id.append( UploadPhoto('outputImages\\narendramodi_5.jpg')['id'])
#    #id.append( UploadPhoto(['outputImages\\narendramodi_4.jpg'])['id'])
#    x = CreateAlbumAndUploadImages('album1-1-1','some description',id)
#    pass

#if __name__ == '__main__':
#    main()