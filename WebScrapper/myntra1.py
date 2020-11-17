# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 16:42:13 2020

@author: Pritam


https://www.myntra.com/gateway/v2/search/kurta-pyjama?f=Categories%3APyjamas&rows=50&o=0
https://www.myntra.com/gateway/v2/search/kurta-pyjama?rows=50&o=0

https://www.myntra.com/gateway/v2/product/2471500/related

https://www.myntra.com/gateway/v2/search/kurta-pyjama?f=Categories%3APyjamas&rows=50&o=0
"""

import requests
from bs4 import BeautifulSoup
import os
import math
import numpy as np
import pandas as pd
import json
from pathlib import Path
path = Path(os.path.dirname(os.path.realpath(__file__)))

htmlstr = """<div class="desktop-pSearchlinks" data-reactid="127"><!-- react-text: 128 --> <!-- /react-text --><a href="/makeup" data-reactid="129"><!-- react-text: 130 --> <!-- /react-text --><!-- react-text: 131 -->Makeup<!-- /react-text --><!-- react-text: 132 --> <!-- /react-text --></a><a href="/girls-dresses" data-reactid="133"><!-- react-text: 134 --> <!-- /react-text --><!-- react-text: 135 -->Dresses For Girls<!-- /react-text --><!-- react-text: 136 --> <!-- /react-text --></a><a href="/tshirts" data-reactid="137"><!-- react-text: 138 --> <!-- /react-text --><!-- react-text: 139 -->T-Shirts<!-- /react-text --><!-- react-text: 140 --> <!-- /react-text --></a><a href="/sandals" data-reactid="141"><!-- react-text: 142 --> <!-- /react-text --><!-- react-text: 143 -->Sandals<!-- /react-text --><!-- react-text: 144 --> <!-- /react-text --></a><a href="/headphones" data-reactid="145"><!-- react-text: 146 --> <!-- /react-text --><!-- react-text: 147 -->Headphones<!-- /react-text --><!-- react-text: 148 --> <!-- /react-text --></a><a href="/babydolls" data-reactid="149"><!-- react-text: 150 --> <!-- /react-text --><!-- react-text: 151 -->Babydolls<!-- /react-text --><!-- react-text: 152 --> <!-- /react-text --></a><a href="/men-blazers" data-reactid="153"><!-- react-text: 154 --> <!-- /react-text --><!-- react-text: 155 -->Blazers For Men<!-- /react-text --><!-- react-text: 156 --> <!-- /react-text --></a><a href="/handbags" data-reactid="157"><!-- react-text: 158 --> <!-- /react-text --><!-- react-text: 159 -->Handbags<!-- /react-text --><!-- react-text: 160 --> <!-- /react-text --></a><a href="/women-watches" data-reactid="161"><!-- react-text: 162 --> <!-- /react-text --><!-- react-text: 163 -->Ladies Watches<!-- /react-text --><!-- react-text: 164 --> <!-- /react-text --></a><a href="/bags" data-reactid="165"><!-- react-text: 166 --> <!-- /react-text --><!-- react-text: 167 -->Bags<!-- /react-text --><!-- react-text: 168 --> <!-- /react-text --></a><a href="/sports-shoes" data-reactid="169"><!-- react-text: 170 --> <!-- /react-text --><!-- react-text: 171 -->Sport Shoes<!-- /react-text --><!-- react-text: 172 --> <!-- /react-text --></a><a href="/reebok-shoes" data-reactid="173"><!-- react-text: 174 --> <!-- /react-text --><!-- react-text: 175 -->Reebok Shoes<!-- /react-text --><!-- react-text: 176 --> <!-- /react-text --></a><a href="/puma-shoes" data-reactid="177"><!-- react-text: 178 --> <!-- /react-text --><!-- react-text: 179 -->Puma Shoes<!-- /react-text --><!-- react-text: 180 --> <!-- /react-text --></a><a href="/men-boxers" data-reactid="181"><!-- react-text: 182 --> <!-- /react-text --><!-- react-text: 183 -->Boxers<!-- /react-text --><!-- react-text: 184 --> <!-- /react-text --></a><a href="/wallets" data-reactid="185"><!-- react-text: 186 --> <!-- /react-text --><!-- react-text: 187 -->Wallets<!-- /react-text --><!-- react-text: 188 --> <!-- /react-text --></a><a href="/women-shirts-tops-tees" data-reactid="189"><!-- react-text: 190 --> <!-- /react-text --><!-- react-text: 191 -->Tops<!-- /react-text --><!-- react-text: 192 --> <!-- /react-text --></a><a href="/earrings" data-reactid="193"><!-- react-text: 194 --> <!-- /react-text --><!-- react-text: 195 -->Earrings<!-- /react-text --><!-- react-text: 196 --> <!-- /react-text --></a><a href="/fastrack-watches" data-reactid="197"><!-- react-text: 198 --> <!-- /react-text --><!-- react-text: 199 -->Fastrack Watches<!-- /react-text --><!-- react-text: 200 --> <!-- /react-text --></a><a href="/women-kurtas-kurtis-suits" data-reactid="201"><!-- react-text: 202 --> <!-- /react-text --><!-- react-text: 203 -->Kurtis<!-- /react-text --><!-- react-text: 204 --> <!-- /react-text --></a><a href="/nike" data-reactid="205"><!-- react-text: 206 --> <!-- /react-text --><!-- react-text: 207 -->Nike<!-- /react-text --><!-- react-text: 208 --> <!-- /react-text --></a><a href="/smart-watches" data-reactid="209"><!-- react-text: 210 --> <!-- /react-text --><!-- react-text: 211 -->Smart Watches<!-- /react-text --><!-- react-text: 212 --> <!-- /react-text --></a><a href="/titan-watches" data-reactid="213"><!-- react-text: 214 --> <!-- /react-text --><!-- react-text: 215 -->Titan Watches<!-- /react-text --><!-- react-text: 216 --> <!-- /react-text --></a><a href="/saree-blouse" data-reactid="217"><!-- react-text: 218 --> <!-- /react-text --><!-- react-text: 219 -->Designer Blouse<!-- /react-text --><!-- react-text: 220 --> <!-- /react-text --></a><a href="/gown" data-reactid="221"><!-- react-text: 222 --> <!-- /react-text --><!-- react-text: 223 -->Gowns<!-- /react-text --><!-- react-text: 224 --> <!-- /react-text --></a><a href="/rings" data-reactid="225"><!-- react-text: 226 --> <!-- /react-text --><!-- react-text: 227 -->Rings<!-- /react-text --><!-- react-text: 228 --> <!-- /react-text --></a><a href="/cricket-shoes" data-reactid="229"><!-- react-text: 230 --> <!-- /react-text --><!-- react-text: 231 -->Cricket Shoes<!-- /react-text --><!-- react-text: 232 --> <!-- /react-text --></a><a href="/forever-21" data-reactid="233"><!-- react-text: 234 --> <!-- /react-text --><!-- react-text: 235 -->Forever 21<!-- /react-text --><!-- react-text: 236 --> <!-- /react-text --></a><a href="/eye-makeup" data-reactid="237"><!-- react-text: 238 --> <!-- /react-text --><!-- react-text: 239 -->Eye Makeup<!-- /react-text --><!-- react-text: 240 --> <!-- /react-text --></a><a href="/photo-frames" data-reactid="241"><!-- react-text: 242 --> <!-- /react-text --><!-- react-text: 243 -->Photo Frames<!-- /react-text --><!-- react-text: 244 --> <!-- /react-text --></a><a href="/punjabi-suits" data-reactid="245"><!-- react-text: 246 --> <!-- /react-text --><!-- react-text: 247 -->Punjabi Suits<!-- /react-text --><!-- react-text: 248 --> <!-- /react-text --></a><a href="/bikini" data-reactid="249"><!-- react-text: 250 --> <!-- /react-text --><!-- react-text: 251 -->Bikini<!-- /react-text --><!-- react-text: 252 --> <!-- /react-text --></a><a href="/shop/myntra-fashion-superstar" data-reactid="253"><!-- react-text: 254 --> <!-- /react-text --><!-- react-text: 255 -->Myntra Fashion Show<!-- /react-text --><!-- react-text: 256 --> <!-- /react-text --></a><a href="/lipstick" data-reactid="257"><!-- react-text: 258 --> <!-- /react-text --><!-- react-text: 259 -->Lipstick<!-- /react-text --><!-- react-text: 260 --> <!-- /react-text --></a><a href="/saree" data-reactid="261"><!-- react-text: 262 --> <!-- /react-text --><!-- react-text: 263 -->Saree<!-- /react-text --><!-- react-text: 264 --> <!-- /react-text --></a><a href="/watches" data-reactid="265"><!-- react-text: 266 --> <!-- /react-text --><!-- react-text: 267 -->Watches<!-- /react-text --><!-- react-text: 268 --> <!-- /react-text --></a><a href="/dresses" data-reactid="269"><!-- react-text: 270 --> <!-- /react-text --><!-- react-text: 271 -->Dresses<!-- /react-text --><!-- react-text: 272 --> <!-- /react-text --></a><a href="/lehengas" data-reactid="273"><!-- react-text: 274 --> <!-- /react-text --><!-- react-text: 275 -->Lehenga<!-- /react-text --><!-- react-text: 276 --> <!-- /react-text --></a><a href="/nike-shoes" data-reactid="277"><!-- react-text: 278 --> <!-- /react-text --><!-- react-text: 279 -->Nike Shoes<!-- /react-text --><!-- react-text: 280 --> <!-- /react-text --></a><a href="/goggles" data-reactid="281"><!-- react-text: 282 --> <!-- /react-text --><!-- react-text: 283 -->Goggles<!-- /react-text --><!-- react-text: 284 --> <!-- /react-text --></a><a href="/bra" data-reactid="285"><!-- react-text: 286 --> <!-- /react-text --><!-- react-text: 287 -->Bras<!-- /react-text --><!-- react-text: 288 --> <!-- /react-text --></a><a href="/men-suits" data-reactid="289"><!-- react-text: 290 --> <!-- /react-text --><!-- react-text: 291 -->Suit<!-- /react-text --><!-- react-text: 292 --> <!-- /react-text --></a><a href="/chinos" data-reactid="293"><!-- react-text: 294 --> <!-- /react-text --><!-- react-text: 295 -->Chinos<!-- /react-text --><!-- react-text: 296 --> <!-- /react-text --></a><a href="/shoes" data-reactid="297"><!-- react-text: 298 --> <!-- /react-text --><!-- react-text: 299 -->Shoes<!-- /react-text --><!-- react-text: 300 --> <!-- /react-text --></a><a href="/adidas-shoes" data-reactid="301"><!-- react-text: 302 --> <!-- /react-text --><!-- react-text: 303 -->Adidas Shoes<!-- /react-text --><!-- react-text: 304 --> <!-- /react-text --></a><a href="/woodland-shoes" data-reactid="305"><!-- react-text: 306 --> <!-- /react-text --><!-- react-text: 307 -->Woodland Shoes<!-- /react-text --><!-- react-text: 308 --> <!-- /react-text --></a><a href="/jewellery" data-reactid="309"><!-- react-text: 310 --> <!-- /react-text --><!-- react-text: 311 -->Jewellery<!-- /react-text --><!-- react-text: 312 --> <!-- /react-text --></a><a href="/designer-saree" data-reactid="313"><!-- react-text: 314 --> <!-- /react-text --><!-- react-text: 315 -->Designers Sarees<!-- /react-text --><!-- react-text: 316 --> <!-- /react-text --></a><!-- react-text: 317 --> <!-- /react-text --></div>"""
soup = BeautifulSoup(htmlstr, "html.parser")

list = []
listresult = soup.findAll("a", href=True)
for index, alink in enumerate(listresult):
    list.append("https://www.myntra.com/gateway/v2/search" +
                alink["href"] + "?rows=50&o=0")

BaseURL = list[0]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
cookies = {"_d_id": "582592e1-d45b-4457-8979-3a1a8c547d80",
           "mynt-eupv": "1",
           "_gcl_au": "1.1.1975410500.1605093967",
           "_ga": "GA1.2.1758249549.1605093968",
           "tvc_VID": "1",
           "_fbp": "fb.1.1605093973749.249597231",
           "at": "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTURZNVptTXlaamd0TWpReU5DMHhNV1ZpTFdFeVpXRXRNREF3WkROaFpqSTRZVFUzSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUyTWpBMk5UUXlOekVzSW1semN5STZJa2xFUlVFaWZRLl9SOW1IdDdjY0ZMZmFGYU80a0pnN2hPR1h2RklzZHRPQkF6TWlDSkRwZE0=",
           "_abck": "9F4F1B92452FD86BEDCAD3EBB684F19D~0~YAAQ7/3UFy8XsYh1AQAAjPuMtwSCaFNaPIfV9eBzPw6+SaIdxQW5ew030rA7gyAKiiJLqMlOSDu6ZYwuW4fT2RcdDdvOHiy2HYsoyr4i17BD+4RIAE0WRCoS3KKPQ1Xh+QpuHqNlRrqSilY0zyvuJt/q5IroVxpllkGtHV8HpQCOuwmaWrBV78U4ft9U1ei89Q7BFlkR9OI4k8sti4j4ZoSDffxEUwZdCQi646uvBaD4TtfnaHybsFhtWhCc5FY1wWPBqy/7IZyWuZHqxa7dURNarEkWzDwbdSvVsSwF3j/l3LM+/zArySeiigwenCPx5o6rP/DjJF7mYEuvdW/DR68iYKe4bg==~-1~-1~-1",
           "G_ENABLED_IDPS": "google",
           "__insp_slim": "1605102288938",
           "__insp_wid": "617845923",
           "__insp_nv": "true",
           "__insp_targlpt": "QnV5IEZJRE8gRElETyBNZW4gUGluayBTb2xpZCBQb2xvIENvbGxhciBTbGltIEZpdCBUIFNoaXJ0IC0gVHNoaXJ0cyBmb3IgTWVuIDI0NzE1MDAgfCBNeW50cmE%3D",
           "__insp_targlpu": "aHR0cHM6Ly93d3cubXludHJhLmNvbS90c2hpcnRzL2ZpZG8tZGlkby9maWRvLWRpZG8tbWVuLXBpbmstc29saWQtcG9sby1jb2xsYXItc2xpbS1maXQtdC1zaGlydC8yNDcxNTAwL2J1eQ%3D%3D",
           "__insp_norec_sess": "true",
           "AKA_A2": "A",
           "bm_sz": "2C065C300D168D04BDB895AD2A021DCD~YAAQDbcsMUuNv3h1AQAAwzkJ1wkZucK6IkjQ4NcZW8+boz4WD+XerrutCPNaWBo/aimGXcocVH5oOjlxWR9K5wnibfvwpmknwkFnYHuBmfkW3OOmMrHe2iwekd0DW2ExG6dDa3/WVxi0UMwxjL//TKhSlxmBF6071cPHphAQBKShuhUNtKQU1qehdURJeKtL",
           "_ma_session": """%7B%22id%22%3A%223c2ba678-c5a5-449b-bbf5-cdc18b13a642-582592e1-d45b-4457-8979-3a1a8c547d80%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D""",
           "_mxab_": "",
           "microsessid": "390",
           "lt_timeout": "1",
           "lt_session": "1",
           "utrid": "eX9DEBMTS0JxFVxeCg9AMCM0NDU1NTQ3MDIkMg%3D%3D.fdf88c47221da5a385ec7d5152fbd90c",
           "_xsrf": "s2G5SUnJW4nrJp6QTAsWRuCLfk0Vh4r2",
           "mynt-ulc-api": "pincode%3A411007",
           "mynt-loc-src": "expiry%3A1605631951827%7Csource%3AIP",
           "_ma_events_sequence": "173",
           "ak_bmsc": "41AD04ECDA7DDA0FAD7AC18103ED2C6F312CB70D174C00002BFAB35FC6273532~pl8w1jCB8oDN3p1p3TKfFife9e5aZjl3+BU/L4y8p53CMHCQPOnP5Zrt75BKpUeXtQ5ukpV5j8YKpC6HftR3qtpKuUmp4Z7Czy2O+SGepAAWo6qif/NNLRdFg08WgJDJvdlOsGcFT+oyXVbQ9apLVwHkX8xSwsFTmreohmWGvlKcKHCQj/AMCQPDhC3AifasGTmsdtsuzdXIhI7DohMUrvXH1I/OWL7rTTfzkr/6soECHrAhakRcVK7BoLK/cjZB+j",
           "AMP_TOKEN": "%24NOT_FOUND",
           "_gid": "GA1.2.1868976283.1605630513",
           "bm_sv": "1D8BF4BC26216576FCB4CE78C541E888~hYL+6KrfrMYPJakaSlt+HsSvhIOrgQgZm1A6xOTgsEGGYFpksYtl/xxc+KNiSsHmmXA7eqKNXPZTtbvEryhS0GSu0pmlxZrKp5KXSDeuC5XB0nHDmb0Jm4An581rtk3JFgIEdB2mOvJZzU5P0jrrfWtvsNQAUZF/ptfrPqxMhFE=",
           "akaas_myntra_SegmentationLabel": "1608223270~rv=88~id=8f1182f65473cc42da0b1dffcc81d5f7~rn=PWA",
           "ak_RT": """z=1&dm=myntra.com&si=fa87b44d-cd2a-4f1f-a9be-bde75742d94a&ss=khm6y4cj&sl=2&tt=nsi&bcn=%2F%2F684d0d37.akstat.io%2F&rl=1&ul=iyal&hd=iyb3"""
           }
# apirespoance = requests.get(BaseURL, headers=headers, cookies=cookies)
