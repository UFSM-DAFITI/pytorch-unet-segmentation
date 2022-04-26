import sys
if __name__ == "__main__":
    import urllib.request

    urllib.request.urlretrieve("https://docs.google.com/uc?export=download&id=1sC_puW3pc6P75KTi2hJxgjgUiZo3zl1Q&confirm=t", "unet.pt")
    urllib.request.urlretrieve("https://docs.google.com/uc?export=download&id=1ucX0HD8JV10GFol7cOXHe5W7GAh176Zo&confirm=t", "metahuman.png")
