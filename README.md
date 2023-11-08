# Image Resizer

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

<img src="./assets/banner.png">

---

Takes an image and a scale factor, and returns the image scaled by the factor. 

---

Stuff done by the service: 
1. Listen for `POST` requests from the [frontend](https://github.com/frontend)
2. Save the image to disk
3. Do a little `convert input_imagee -resize scale% output_image`. `convert` command is available to install on most linux distros
4. Send the scaled image back
5. After the request is done, send the orginal image to the [storage service](https://github.com/tusqasi/distributed-storage), along with the user_id and scale factor to be put away for later use


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


## Running 

```bash
 uvicorn app:app --reload
```
