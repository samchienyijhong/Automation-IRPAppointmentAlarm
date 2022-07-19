# JUST AN IRP APPOINTMENT MAKER (No longer usable 🥲)

## Only work for non family application with passport ID

### Inorder to make fake-useragent run properly (avoid IndexError: list index out of range)
#### open /usr/local/lib/python3.9/dist-packages/fake_useragent/utils.py in your favorite text editor using admin privileges. Go to line 99, and change the w3

    html = html.split('<table class="w3-table-all notranslate">')[1]
#### to ws:

    html = html.split('<table class="ws-table-all notranslate">')[1]
#### Reference: https://stackoverflow.com/questions/68772211/fake-useragent-module-not-connecting-properly-indexerror-list-index-out-of-ra

1. Download selenium from https://chromedriver.chromium.org/downloads
2. Define your environment variables in .env file
3. Set your information accordingly (line 64, 83)
4. If your IP get block, you'll need to use your chrome profile installed with VPN extension (line 26) 
