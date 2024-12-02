from workbench.chakin.chakin import Chakin

def main():
    chakin = Chakin()
    # Example usage
    available_vectors = chakin.search(lang='English')
    print("Available vectors:", available_vectors)

    chakin.download(index=0, saveDir='./')

if __name__ == "__main__":
    main()