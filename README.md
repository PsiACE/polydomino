# polydomino

> Every day of life will be a surprise and a miracle.

The goal is to implement a content-based image retrieval system that supports multiple methods. Of course, it is mainly a demonstration rather than a real-world application.

**Note:** This is not a complete project, it exists as a homework for *HZAU Summer Training 2020 - Content Based Image Retrieval*.

## Status

**Simple Demo**, just repeat two tutorials of pyImageSearch. Lack of availability and quality assurance.

## TODO

- [ ] Refactor to rationalize code.
- [ ] More reasonable work flow, minimize manual operation.
- [ ] More effective search. 
    - [x] Support uploading files 
    - [ ] Randomly selecting pictures in the gallery.
    - [ ] Improve retrieval speed.
    - [x] Support more search methods.
- [x] Better UI.
- [ ] Access Control.
- [ ] Others - Basic Guides. (?)

## Usage

Since the project is not yet perfect, here is only an overview of the process rather than specific steps.

1. Clone this repository. `git clone git@github.com:PsiACE/polydomino.git`
2. Put the images (**JPG Only**) into the dataset folders.
3. Index pictures. `python polydomino/index.py --dataset "dataset/*" --index mse.csv --method mse`
4. Select pictures to search.

    - For web, you should edit `.env` to choose algo. Then run `python polydomino/app.py`
    - For cli, just one line like this `python polydomino/search.py --index polydomino/mse.csv --query 0007.jpg --features mse  --searcher mse`

## Features

Feature extraction algorithms include: 3D-HSV Histogram, Color Moments, Gray Matrix, dHash, Hu Moments, etc.

Search algorithm based on statistical method: Euclidean Distance, Manhattan Distance, Hamming Distance, Cosine Similarity, Pearson Similarity, Spearman Similarity, etc.

## Contact

Chojan Shang - [@PsiACE](https://github.com/psiace) - <psiace@outlook.com>

Project Link: [https://github.com/psiace/polydomino](https://github.com/psiace/polydomino)

## License

Licensed under MIT license ([LICENSE](./LICENSE) or [http://opensource.org/licenses/MIT](http://opensource.org/licenses/MIT))

## Acknowledge

Two Tutorials by [pyImageSearch](https://www.pyimagesearch.com/)

1. [Adding a web interface to our image search engine with Flask](http://www.pyimagesearch.com/2014/12/08/adding-web-interface-image-search-engine-flask/)
2. [The complete guide to building an image search engine with Python and OpenCV](http://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/)
