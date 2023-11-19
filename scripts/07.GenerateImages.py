import os.path
from PIL import Image
import base64
from io import BytesIO
import requests

from includes.constants import ROOT_PATH

url = "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image"
pages_file_path = 'all_dirs.txt'
save_folder = ROOT_PATH + '_img/pages/'

cost = 0
cnt = 1
with open(pages_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        stripped = line.strip()
        save_folder = ROOT_PATH + '_img/pages/' + stripped
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        slug = stripped.rstrip('/').split('/')[-1]
        cats = stripped.replace('-', ' ').rstrip('/').split('/')
        prompt = 'bundle of products'
        cats.reverse()
        for cat in cats:
            prompt += ' under ' + cat + ' category'
        prompt += '. realistic style.'

        payload = {
            "model": "stable-diffusion-xl-v1-0",
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "steps": 10,
            "guidance": 7,
            "output_format": "png"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer key-4WZdungVYt2qs66fETH0S95myr1GNMHbEW17qFXZnGMrhlg9b6tlwIhcCLfVnQgsm8XfH9hrRinusWRNEkjt49niugWiehmL"
        }

        save_path = save_folder + slug + '.webp'
        if not os.path.exists(save_path):
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            cost += data['cost']
            decoded = base64.b64decode(data['image'])
            img = Image.open(BytesIO(decoded))
            img.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT).save(save_path)

            # Crop image
            crop_cnt = 1
            for i in range(0, 1024, 256):
                left = 0
                top = i
                right = 1024
                bottom = i + 256

                cropped = img.crop((left, top, right, bottom))
                save_path = save_folder + slug + '-' + str(crop_cnt) + '.webp'
                if not os.path.exists(save_path):
                    cropped.save(save_path)

                crop_cnt += 1
        
        print('Processed:', cnt, save_folder)
        print('Cost: $' + str(cost))
        cnt += 1

print('DONE. TOTAL COST: $' + str(cost))
