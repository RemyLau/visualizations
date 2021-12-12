# visualizations

## Installation

Follow the instruction on the [installation](https://docs.manim.community/en/stable/installation/macos.html)
page by the [Manim Community](https://docs.manim.community/en/stable/index.html)
to install [Manim](https://pypi.org/project/manim/) on MacOS. In short:

```bash
# Optionally, create a virtual env for manim
conda create -n manim python=3.8 -y && conda activate manim

# Install required dependencies for Manim
brew install py3cairo ffmpeg

# Required for Apple Silicon based machines
brew install cmake pango scipy

# Finally, install Manim
pip install manim

# Optionally, install dependencies for rending LaTex
brew install --cask mactex
```
