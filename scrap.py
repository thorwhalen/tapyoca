
if __name__ == '__main__':
    
    from importlib.resources import files

    f = files('tapyoca')
    print(f"{f=}")

    from pkg_resources import resource_filename

    ff = resource_filename('tapyoca')
    print(f"{ff=}")


