import os
from google.colab.output import eval_js
os.environ['colab_url'] = eval_js("google.colab.kernel.proxyPort(7860, {'cache': false})")

!apt -y update -qq
!wget http://launchpadlibrarian.net/367274644/libgoogle-perftools-dev_2.5-2.2ubuntu3_amd64.deb
!wget https://launchpad.net/ubuntu/+source/google-perftools/2.5-2.2ubuntu3/+build/14795286/+files/google-perftools_2.5-2.2ubuntu3_all.deb
!wget https://launchpad.net/ubuntu/+source/google-perftools/2.5-2.2ubuntu3/+build/14795286/+files/libtcmalloc-minimal4_2.5-2.2ubuntu3_amd64.deb
!wget https://launchpad.net/ubuntu/+source/google-perftools/2.5-2.2ubuntu3/+build/14795286/+files/libgoogle-perftools4_2.5-2.2ubuntu3_amd64.deb
!apt install -qq libunwind8-dev
!dpkg -i *.deb
%env LD_PRELOAD=libtcmalloc.so
!rm *.deb

!apt -y install -qq aria2
!pip install -q https://github.com/camenduru/stable-diffusion-webui-colab/releases/download/0.0.16/xformers-0.0.16+814314d.d20230118-cp38-cp38-linux_x86_64.whl
!pip install -q --pre triton

!git clone -b v1.6 https://github.com/camenduru/stable-diffusion-webui
!wget https://raw.githubusercontent.com/camenduru/stable-diffusion-webui-scripts/main/run_n_times.py -O /content/stable-diffusion-webui/scripts/run_n_times.py
!git clone -b v1.6 https://github.com/camenduru/deforum-for-automatic1111-webui /content/stable-diffusion-webui/extensions/deforum-for-automatic1111-webui
!git clone -b v1.6 https://github.com/camenduru/stable-diffusion-webui-images-browser /content/stable-diffusion-webui/extensions/stable-diffusion-webui-images-browser
!git clone -b v1.6 https://github.com/camenduru/stable-diffusion-webui-huggingface /content/stable-diffusion-webui/extensions/stable-diffusion-webui-huggingface
!git clone -b v1.6 https://github.com/camenduru/sd-civitai-browser /content/stable-diffusion-webui/extensions/sd-civitai-browser
!git clone -b v1.6 https://github.com/camenduru/sd-webui-additional-networks /content/stable-diffusion-webui/extensions/sd-webui-additional-networks
!git clone -b v1.6 https://github.com/camenduru/sd-webui-tunnels /content/stable-diffusion-webui/extensions/sd-webui-tunnels
%cd /content/stable-diffusion-webui
!git reset --hard

!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://onemanager.xsms.ga/chilloutmix_NiPrunedFp32Fix.safetensors -d /content/stable-diffusion-webui/models/Stable-diffusion -o chilloutmix_NiPrunedFp32Fix.safetensors
!wget https://github.com/wibus-wee/stable_diffusion_chilloutmix_ipynb/releases/download/koreanDollLikeness/koreanDollLikeness_v15.safetensors -P /content/stable-diffusion-webui/models/Lora

!sed -i -e '''/    prepare_environment()/a\    os.system\(f\"""sed -i -e ''\"s/self.logvar\\[t\\]/self.logvar\\[t.item()\\]/g\"'' /content/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/models/diffusion/ddpm.py""")''' /content/stable-diffusion-webui/launch.py
!sed -i -e '''/    prepare_environment()/a\    os.system\(f\"""sed -i -e ''\"s/dict()))/dict())).cuda()/g\"'' /content/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/util.py""")''' /content/stable-diffusion-webui/launch.py
!sed -i '$a fastapi==0.90.0' requirements_versions.txt
!sed -i -e 's/default_enabled=False/default_enabled=True/' /content/stable-diffusion-webui/webui.py

!python launch.py --share --xformers --enable-insecure-extension-access --theme dark --cloudflared
