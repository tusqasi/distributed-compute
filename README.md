# Image Resizer

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

<img src="./assets/banner.png">

---

Takes an image and a scale factor, and returns the image scaled by the factor. 

---

Stuff done by the service: 
1. Listen for `POST` requests from the
2. Do a little operation with Pillow
3. Send the scaled image back

## Routes
POST `/scale`  
Takes a `file` which is a image file and a `scale` parameter.

## Requirments 

Go get [`asdf-vm`](https://asdf-vm.com)

```bash
asdf plugin-add python
asdf install
pip install -r requirments.txt
```


## Running 

```bash
 uvicorn app:app --reload
```
