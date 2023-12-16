from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.kalibrr.id/home')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'k-container k-grid k-grid-cols-1 md:k-grid-cols-2 xl:k-grid-cols-3 k-gap-4 k-mt-8 k-mb-10'})
row = table.find_all('h2', attrs={'class':'k-w-48 lg:k-w-full k-text-2xl k-font-medium k-font-bold k-text-ellipsis k-overflow-hidden k-whitespace-normal css-1gzvnis'})

row_length = len(row)

soup.find('span', attrs={'class':'k-text-gray-500'})
span = table.find_all('span', attrs={'class':'k-text-gray-500'})
post_span = []
for i in range(2, len(span), 3):
    post_span.append(span[i])

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here

    job_title = table.find_all('h2', attrs={'class':'k-w-48 lg:k-w-full k-text-2xl k-font-medium k-font-bold k-text-ellipsis k-overflow-hidden k-whitespace-normal css-1gzvnis'})[i].text
    
    location = table.find_all('span', attrs={'class':'k-text-gray-500 k-block k-pointer-events-none'})[i].text
    
    post_date = post_span[i].text
    
    deadline = table.find_all('span', attrs={'class':'k-text-xs k-font-bold k-text-gray-600'})[i].text

    company = table.find_all('a', attrs={'class':'k-text-subdued k-font-bold'})[i].text

    temp.append((job_title,location,post_date,deadline,company)) 

#temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('job_title','location','post_date','deadline','company'))

#insert data wrangling here
df['company'] = df['company'].astype('category')
df['location']= df['location'].astype('category')
df['job_title']=df['job_title'].astype('category')
df['location'] = df['location'].str.split(',').str[0]
df_location = pd.DataFrame(df.groupby('location')['job_title'].count())
df_location.rename(columns={'job_title': 'job_amount'}, inplace=True)
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["location"].count()}' #be careful with the " and ' 

	# generate plot
	ax = df_location.sort_values('job_amount').plot(kind= 'barh', figsize = (8,4)) 

	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)