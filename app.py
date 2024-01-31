# app.py
from flask import Flask, render_template, request
from flask import Flask, render_template, request
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

products = [
        #shoe1 shoes
        {'id': 'shoe1', 'name': 'shoe high heels', 'image': 's2.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'shoe good look', 'image': 's4.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'Product A', 'image': 's6.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'Product A', 'image': 's8.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'Product A', 'image': 's10.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'Product A', 'image': 's12.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'Product A', 'image': 's16.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'Product A', 'image': 's18.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'Product A', 'image': 's14.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe1', 'name': 'Product A', 'image': 's20.jpg', 'description': 'Shoe light weight and comfortable.'},

        {'id': 'shoe2', 'name': 'Product B', 'image': 's3.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's5.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's7.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's9.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's11.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's13.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's15.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's17.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's19.jpg', 'description': 'Stylish belt for any occasion.'},
        {'id': 'shoe2', 'name': 'Product B', 'image': 's21.jpg', 'description': 'Stylish belt for any occasion.'},



        {'id': 'shoe3', 'name': 'Product C', 'image': 's22.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's23.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's24.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's25.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's26.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's27.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's28.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's29.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's30.jpg', 'description': 'Elegant and durable watch.'},
        {'id': 'shoe3', 'name': 'Product C', 'image': 's31.jpg', 'description': 'Elegant and durable watch.'},




    #sarees saree1
    {'id': 'saree1', 'name': 'saree', 'image': 'saree1.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree2.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree3.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree4.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree5.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree6.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree7.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree8.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree9.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'saree', 'image': 'saree10.jpg', 'description': 'Beautiful like a wow sarees'},

    {'id': 'saree2', 'name': 'saree', 'image': 'saree11.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree12.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree13.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree14.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree15.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree16.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree17.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree18.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree19.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree20.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'saree', 'image': 'saree21.jpg', 'description': 'good silk sarees'},

    {'id': 'saree3', 'name': 'saree', 'image': 'saree22.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree23.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree24.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree25.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree26.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree27.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree28.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree29.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree30.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree12.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'saree', 'image': 'saree15.jpg', 'description': 'benaras pattu'},

    #watches
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches1.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches2.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches3.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches4.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches5.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches6.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches7.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches8.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches9.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'saree', 'image': 'Watches10.jpg', 'description': 'leather belt watches'},

    {'id': 'watch2', 'name': 'saree', 'image': 'Watches11.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches12.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches13.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches14.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches15.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches16.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches17.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches18.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches19.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'saree', 'image': 'Watches20.jpg', 'description': 'steel belt watches'},

    {'id': 'watch3', 'name': 'saree', 'image': 'Watches21.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches22.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches23.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches24.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches25.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches26.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches27.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches28.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches29.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'saree', 'image': 'Watches30.jpg', 'description': 'smart watches'},

    #tv
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv1.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv2.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv3.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv4.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv5.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv6.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv7.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv8.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv9.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'tv', 'image': 'Tv10.jpg', 'description': 'LED TV'},

    {'id': 'TV2', 'name': 'tv', 'image': 'Tv11.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv12.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv13.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv14.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv15.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv16.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv17.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv18.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv19.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'tv', 'image': 'Tv20.jpg', 'description': 'DOOM TV'},

    {'id': 'TV3', 'name': 'tv', 'image': 'Tv21.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv22.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv23.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv24.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv25.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv26.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv27.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv28.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv29.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'tv', 'image': 'Tv30.jpg', 'description': 'SMART TV'},

    #mencloth
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men1.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men2.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men3.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men4.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men5.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men6.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men7.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men8.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men9.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'saree', 'image': 'men10.jpg', 'description': 'torn cloth'},

    {'id': 'mencloth2', 'name': 'saree', 'image': 'men11.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men12.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men13.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men14.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men15.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men16.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men17.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men18.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men19.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'saree', 'image': 'men20.jpg', 'description': 'bloody clothing pvt.ltd'},

    {'id': 'mencloth3', 'name': 'saree', 'image': 'men21.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men22.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men23.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men24.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men25.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men26.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men27.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men28.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men29.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'saree', 'image': 'men30.jpg', 'description': 'once tried always used'},


#Laptops
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop1.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop2.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop3.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop4.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop5.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop6.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop7.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop8.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop9.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop10.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop11.jpg', 'description': 'Idea pad'},

    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop12.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop13.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop`4.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop15.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop16.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop17.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop17.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop18.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop19.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop20.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop21.jpg', 'description': 'viva book'},

    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop22.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop23.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop24.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop25.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop26.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop27.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop28.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop29.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop30.jpg', 'description': 'note book'},


#dining
    {'id': 'din1', 'name': 'din', 'image': 'DT1.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT2.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT3.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT4.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT5.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT6.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT7.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT8.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT9.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT10.jpg', 'description': 'note book'},

    {'id': 'din2', 'name': 'dint', 'image': 'DT11.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT12.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT13.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT`14.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT15.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT16.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT17.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT18.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT19.jpg', 'description': 'note book'},

    {'id': 'din3', 'name': 'dint', 'image': 'DT20.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT21.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT22.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT23.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT24.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT25.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT26.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT27.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT28.jpg', 'description': 'note book'},
{'id': 'din1', 'name': 'din', 'image': 'DT29.jpg', 'description': 'note book'},
        {'id': 'din2', 'name': 'dint', 'image': 'DT30.jpg', 'description': 'note book'},
        {'id': 'din3', 'name': 'dint', 'image': 'DT1.jpg', 'description': 'note book'},

        {'id': 'VAS1', 'name': 'din', 'image': 'v1.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v11.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v12.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v13.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v14.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v15.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v16.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v17.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v18.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v19.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v20.jpg', 'description': 'note book'},

    {'id': 'VAS2', 'name': 'dint', 'image': 'v2.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v3.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v4.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v5.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v6.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v7.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v8.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v9.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v10.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v13.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v.20jpg', 'description': 'note book'},

    {'id': 'VAS3', 'name': 'dint', 'image': 'v21.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v22.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v23.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v24.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v25.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v26.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v27.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v28.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v29.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v30.jpg', 'description': 'note book'},


#washes
    {'id': 'WAS1', 'name': 'din', 'image': 'wm1.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm10.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm11.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm12.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm13.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm14.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm15.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm16.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm17.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm18.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm19.jpg', 'description': '10kg'},

    {'id': 'WAS2', 'name': 'dint', 'image': 'wm20.jpg', 'description': '20kg'},

    {'id': 'WAS2', 'name': 'dint', 'image': 'wm21.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm22.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm23.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm24.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm25.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm26.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm27.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm28.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm29.jpg', 'description': '20kg'},

    {'id': 'WAS3', 'name': 'dint', 'image': 'wm30.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm2.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm3.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm4.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm5.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm6.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm7.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm8.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm9.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm10.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm17.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm19.jpg', 'description': '30kg'}

    # Add more products as needed
    ]
# Load the language detection model
language_model = load_model(r"D:\pythonana\mspr\langs\language_id_model.h5")

import pickle

# Load the tokenizer
with open(r"D:\pythonana\mspr\langs\tokenizer.pickle", 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the label encoder
with open(r"D:\pythonana\mspr\langs\label_encoder.pickle", 'rb') as handle:
    label_encoder = pickle.load(handle)

# Load the telugu sentiment analysis model and vectorizer
telugu_vectorizer = joblib.load(r'D:\pythonana\mspr\telugu_vectorizer.pkl')
telugu_sentiment_model = joblib.load(r'D:\pythonana\mspr\telugu_sentiment_model.pkl')

# Load the hindi sentiment analysis model and vectorizer
hindi_vectorizer = joblib.load(r'D:\pythonana\mspr\hindi_vectorizer.pkl')
hindi_sentiment_model = joblib.load(r'D:\pythonana\mspr\hindi_sentiment_model.pkl')

# Load the English sentiment analysis model and vectorizer
english_vectorizer = joblib.load(r'D:\pythonana\mspr\english_vectorizer.pkl')
english_sentiment_model = joblib.load(r'D:\pythonana\mspr\english_sentiment_model.pkl')

app = Flask(__name__)

# Placeholder function for sentiment analysis
def identify_language(text):
    input_sequence = tokenizer.texts_to_sequences([text])
    input_sequence = pad_sequences(input_sequence, maxlen=102)
    predicted_probabilities = language_model.predict(input_sequence)
    predicted_language_index = np.argmax(predicted_probabilities)
    predicted_language = label_encoder.classes_[predicted_language_index]
    return predicted_language

def perform_sentiment_analysis(text,language):
    # Replace this with your sentiment analysis logic
    # Return 'positive', 'negative', or 'neutral'
    if language == 'Telugu':
        text_vectorized = telugu_vectorizer.transform([text])
        predicted_sentiment = telugu_sentiment_model.predict(text_vectorized)[0]
    elif language == 'Hindi':
        text_vectorized = hindi_vectorizer.transform([text])
        predicted_sentiment = hindi_sentiment_model.predict(text_vectorized)[0]
    else:
        text_vectorized = english_vectorizer.transform([text])
        predicted_sentiment = english_sentiment_model.predict(text_vectorized)[0]
    return predicted_sentiment
    # return 'positive'

# Placeholder function for product recommendation
def get_recommendations(s, id):#sentiment,product_id
    # Replace this with your product recommendation logic
    # Return a list of recommended products
    pl=[]
    nl=[]
    neutl=[]
    # return products
    if 'shoe' in id:

        if id =='shoe1':
            if s.lower()=='positive':
                return products[0:20:2]
            elif s.lower()=='negative':
                return products[1:20:2]+products[20:30]
            return products[10:13]+products[2:5]+products[18:30]+products[13:18]

        elif id=='shoe2':
            if s.lower()=='positive':
                return products[1:20:2]
            elif s.lower()=='negative':
                return products[0:20:2]+products[20:30]
            return products[10:13]+products[2:5]+products[18:30]+products[5:10]

        else:
            if s.lower()=='positive':
                return products[20:30]
            elif s.lower()=='negative':
                return products[0:20]
            return products[10:13]+products[1:10]+products[20:22]+products[13:18]

        #incase of sarees
    elif 'saree' in id:

        if id == 'saree1':
            if s.lower() == 'positive':
                return products[31:41]
            elif s.lower() == 'negative':
                return products[42:63]
            return products[31:33] + products[41:55]

        elif id == 'saree2':
            if s.lower() == 'positive':
                return products[42:51]
            elif s.lower() == 'negative':
                return products[31:41] + products[52:63]
            return products[45:49] + products[31:41] + products[52:62]

        else:
            if s.lower() == 'positive':
                return products[52:63]
            elif s.lower() == 'negative':
                return products[32:62]
            return products[31:56]

        #watch
    elif 'watch' in id:

        if id == 'watch1':
            if s.lower() == 'positive':
                return products[64:73]
            elif s.lower() == 'negative':
                return products[74:93]
            return products[74:93] + products[70:74]

        elif id == 'watch2':
            if s.lower() == 'positive':
                return products[74:85]
            elif s.lower() == 'negative':
                return products[64:73]+products[85:93]
            return products[74:79] + products[64:74]+products[87:92]

        else:
            if s.lower() == 'positive':
                return products[85:93]
            elif s.lower() == 'negative':
                return products[74:85]
            return products[74:85] + products[90:94]

    #tv
    elif 'TV' in id:

        if id == 'TV1':
            if s.lower() == 'positive':
                return products[94:105]
            elif s.lower() == 'negative':
                return products[105:125]
            return products[96:102] + products[105:124]

        elif id == 'TV2':
            if s.lower() == 'positive':
                return products[105:115]
            elif s.lower() == 'negative':
                return products[100:105] +products[116:125]
            return products[96:109] + products[115:124]

        else:
            if s.lower() == 'positive':
                return products[115:125]
            elif s.lower() == 'negative':
                return products[95:115]
            return products[96:118]

    elif 'mencloth' in id:

        if id == 'mencloth1':
            if s.lower() == 'positive':
                return products[124:137]
            elif s.lower() == 'negative':
                return products[137:157]
            return products[134:153]# + products[105:124]

        elif id == 'mencloth2':
            if s.lower() == 'positive':
                return products[134:143]
            elif s.lower() == 'negative':
                return products[148:153]+products[124:134]
            return products[139:153]

        else:
            if s.lower() == 'positive':
                return products[144:153]
            elif s.lower() == 'negative':
                return products[127:147]
            return products[127:150]

    elif 'lap' in id:

        if id == 'lap1':
            if s.lower() == 'positive':
                return products[157:167]
            elif s.lower() == 'negative':
                return products[167:186]
            return products[162:186]# + products[105:124]

        elif id == 'lap2':
            if s.lower() == 'positive':
                return products[167:177]
            elif s.lower() == 'negative':
                return products[177:186]+products[157:163]
            return products[162:186]

        else:
            if s.lower() == 'positive':
                return products[177:187]
            elif s.lower() == 'negative':
                return products[157:176]# + products[157:163]
            return products[158:182]

    elif 'din' in id:

        if id == 'din1':
            if s.lower() == 'positive':
                return products[187:197]
            elif s.lower() == 'negative':
                return products[197:216]
            return products[192:216]

        elif id == 'din2':
            if s.lower() == 'positive':
                return products[197:207]
            elif s.lower() == 'negative':
                return products[187:196]+products[206:216]
            return products[187:199]+products[210:216]

        else:
            if s.lower() == 'positive':
                return products[207:217]
            elif s.lower() == 'negative':
                return products[187:206]
            return products[187:210]

    elif 'VAS' in id:

        if id == 'VAS1':
            if s.lower() == 'positive':
                return products[217:227]
            elif s.lower() == 'negative':
                return products[227:246]
            return products[222:246]

        elif id == 'VAS2':
            if s.lower() == 'positive':
                return products[227:237]
            elif s.lower() == 'negative':
                return products[217:226]+products[237:246]
            return products[218:232]+products[236:246]

        else:
            if s.lower() == 'positive':
                return products[237:247]
            elif s.lower() == 'negative':
                return products[217:236]
            return products[219:239]


    elif 'WAS' in id:

        if id == 'WAS1':
            if s.lower() == 'positive':
                return products[247:257]
            elif s.lower() == 'negative':
                return products[257:276]
            return products[252:276]


        elif id == 'WAS2':
            if s.lower() == 'positive':
                return products[257:267]
            elif s.lower() == 'negative':
                return products[267:276]+products[247:257]
            return products[248:259]+products[265:275]

        else:
            if s.lower() == 'positive':
                return products[257:275]
            elif s.lower() == 'negative':
                return products[247:267]
            return products[247:270]






    return [id]


@app.route('/')
def index():
    pd=[
        {'id': 'shoe1', 'name': 'Product A', 'image': 's2.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe2', 'name': 'Product b', 'image': 's3.jpg','description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe3', 'name': 'Product c', 'image': 's24.jpg','description': 'Shoe light weight and comfortable.'},


        {'id': 'saree1', 'name': 'saree', 'image': 's31.jpg', 'description': 'Beautiful like a wow sarees'},
        {'id': 'saree2', 'name': 'saree', 'image': 's31.jpg', 'description': 'good silk sarees'},
        {'id': 'saree3', 'name': 'saree', 'image': 's31.jpg', 'description': 'benaras pattu'},


        {'id': 'watch1', 'name': 'saree', 'image': 's31.jpg', 'description': 'leather belt watches'},
        {'id': 'watch2', 'name': 'saree', 'image': 's31.jpg', 'description': 'steel belt watches'},
        {'id': 'watch3', 'name': 'saree', 'image': 's31.jpg', 'description': 'smart watches'},

        {'id': 'TV1', 'name': 'saree', 'image': 's31.jpg', 'description': 'LED TV'},
        {'id': 'TV2', 'name': 'saree', 'image': 's31.jpg', 'description': 'DOOM TV'},
        {'id': 'TV3', 'name': 'saree', 'image': 's31.jpg', 'description': 'SMART TV'},

        {'id': 'mencloth1', 'name': 'saree', 'image': 'men1.jpg', 'description': 'torn cloth'},
        {'id': 'mencloth2', 'name': 'saree', 'image': 'men2.jpg', 'description': 'torn cloth'},
        {'id': 'mencloth3', 'name': 'saree', 'image': 'men3.jpg', 'description': 'torn cloth'},

        {'id': 'lap1', 'name': 'lapt', 'image': 'lap.jpg', 'description': 'Idea pad'},
        {'id': 'lap2', 'name': 'lapt', 'image': 'lap.jpg', 'description': 'viva book'},
        {'id': 'lap3', 'name': 'lapt', 'image': 'lap.jpg', 'description': 'note book'},

        {'id': 'din1', 'name': 'din', 'image': 'DT.jpg', 'description': 'note book'},
        {'id': 'din2', 'name': 'dint', 'image': 'DT.jpg', 'description': 'note book'},
        {'id': 'din3', 'name': 'dint', 'image': 'DT.jpg', 'description': 'note book'},

        {'id': 'VAS1', 'name': 'din', 'image': 'v1.jpg', 'description': 'note book'},
        {'id': 'VAS2', 'name': 'dint', 'image': 'v.jpg', 'description': 'note book'},
        {'id': 'VAS3', 'name': 'dint', 'image': 'v.jpg', 'description': 'note book'},

        {'id': 'WAS1', 'name': 'din', 'image': 'wm1.jpg', 'description': 'note book'},
        {'id': 'WAS2', 'name': 'dint', 'image': 'wm.jpg', 'description': 'note book'},
        {'id': 'WAS3', 'name': 'dint', 'image': 'wm.jpg', 'description': 'note book'}

    ]
    # return render_template('index.html')
    # return render_template('index.html')
    return render_template('index.html', pd=pd,products=products)

@app.route('/analyze', methods=['POST'])
def analyze():
    # product = request.form['product']
    # review = request.form['review']
    # product_id = request.form.get('product_id')
    # product = request.form.get('product')
    # product_id = request.form['product_id']
    product_id = request.form.get('id')
    # product = request.form.get('product')
    # review = request.form.get('review')

    if request.method == 'POST':
        text = request.form['review']
        language = identify_language(text)
        sentiment = perform_sentiment_analysis(text, language)
        recommendations = get_recommendations(sentiment, product_id)
        # return render_template('index.html', text=text, language=language, sentiment=sentiment)
        return render_template('result.html', sentiment=sentiment, recommendations=recommendations,product_id=product_id)


    # Perform product recommendation based on the sentiment and selected product



if __name__ == '__main__':
    app.run(debug=True)
