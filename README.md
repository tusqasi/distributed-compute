# Image Resizer

Takes an image and a scale factor, and returns the image scaled by the factor. 


Stuff done 
1. Listen for `POST` requests
2. Save the image to disk
3. Do a little `convert input_imagee -resize scale% output_image`. `convert` command is available to install on most linux distros.


## Routes
POST `/scale`
Takes a `file` which is a image file and a `scale` parameter.

## Requirments 

Go get `asdf-vm`

```bash
asdf plugin-add python
asdf install
pip install -r requirments.txt
```
