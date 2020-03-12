## Simplest Russian NRE (Flask+Angular+Docker Compose).Tags: ORG,LOC,PER

## To Run:
1. In project folder input:   ***sudo docker-compose up --build*** <br>
2. Go to http://localhost:4200/
3. Try it!

> ## About:
> As basis was taken "Lenta.ru" + "DeepPavlov BERT NER" ([data set here](https://drive.google.com/file/d/1JjabV7ESASYgEz28E8LqENE-It0CRVnA/view?usp=sharing)) in json lines format (jsonl) data sets which shape in common is about 740.000 sentences.Every sentence looks like:</br>
> ![alt_text](https://github.com/HronoSF/DCIR_2018_19/blob/master/NRE%20(FP)/pictures/common_look_jsonl.jpg)</br>
> Than it was transformated in csv with defined structure: 
> #### sentence number -> word -> part of speach -> tag ####
> ![alt text](https://github.com/HronoSF/DCIR_2018_19/blob/master/NRE%20(FP)/pictures/csv_structure.jpg)
>> ## Model: ##
>> #### IF YOU HAVE STRONG DEVICE - INCREASE NUMBERS OF EPOCHS AND PLAY WITH HYPER PARAMS </br> TO GET BETTER PREDICTION RESULT (EPOCHS = 200 , BATCH_SIZE = 750 , FOR EXAMPLE) 
>> As model was choosen classic for this type of NLP problems model - ***Bidirectional LSTM-CRF*** ([look here](https://arxiv.org/pdf/1508.01991v1.pdf)): 
>> ![alt text](https://github.com/HronoSF/DCIR_2018_19/blob/master/NRE%20(FP)/pictures/Screenshot%20from%202019-12-21%2015-47-38.png)</br>
>> Here you can see result of training on 5 epochs and data set of 200.000 sentences:</br>
![alt text](https://github.com/HronoSF/DCIR_2018_19/blob/master/NRE%20(FP)/pictures/results.png)
>>> ## Possibility model improvemets: ###
>>>***1)*** use an embedding layer for POS tags concatenated with word embeddings:</br>
>>>```python
>>>input = Input(shape=(max_len,))
>>>word_emb = Embedding(input_dim=n_words + 1, output_dim=20,
>>>input_length=max_len, mask_zero=True)(input) # 20-dim embedding
>>>
>>>pos_input = Input(shape=(max_len,))
>>>pos_emb = Embedding(input_dim= len(pos_tags) , output_dim=10,input_length=max_len, mask_zero=True)(pos_input)
>>>
>>>model =keras.layers.Concatenate()([word_emb, pos_emb])
>>>
>>>model = Bidirectional(LSTM(units=50, return_sequences=True,recurrent_dropout=0.1))(model)
> ## If you want learn model on full data set and use it, you need to do: ###
> 1. Preprocess all data set,train model and save it.You can do it in [this notebook](https://github.com/HronoSF/DC_2018_19/blob/master/Final%20Project/NER.ipynb)
> 2. Get saved files and put each in [resources folder in backend](https://github.com/HronoSF/DC_2018_19/tree/master/Final%20Project/flask-back/resources)
> 3. Restart and rebuild backend docker container ( ***sudo docker-compose up flask-back --build*** or run application again as described upper)
