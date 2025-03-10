import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import django
four_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(four_levels_up)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pi_dashboard.settings')
django.setup()
import pandas as pd
import argparse
from dashboard.models import *
from wordcloud import WordCloud
import mpld3


def generate_wordcloud(amount = 20, dataset = None, path_to_save = "src/dashboard/views/chart_generator_scripts", output_name = 'wordcloud'):
    if dataset is None:
        raise ValueError("No dataset provided.")
        
    if path_to_save is None:
        path_to_save = "src/dashboard/static"
    
    if output_name is None:
        output_name = 'wordcloud.png'

    # Convert the DataFrame to a dictionary {word: frequency}
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dataset)

    # Plot the word cloud using matplotlib
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    file_path = path_to_save + '/'+ output_name +'.png'
    fig.savefig(file_path, format='png')

    # Disable the axis and grid in mpld3 as well
    mpld3.plugins.clear(fig)  # Remove any mpld3 default plugins
    html_str = mpld3.fig_to_html(fig)
    
def main(amount, dataset, path_to_save, output_name):
    if amount is None:
        amount = 20
    if dataset is None:
        generate_wordcloud(amount, path_to_save, output_name)
    dataset = json.loads(dataset)
    generate_wordcloud(amount, dataset, path_to_save, output_name)
    
    
""" dataset = list(Tf_Idf.objects.all().values('palavra', 'tf_idf')[:20]) 
dict_dataset = {entry['palavra']: entry['tf_idf'] for entry in dataset}
dict_dataset = {'pompa':0,
                'circuito':1,
                'eletrico':2,
                'bisnaga':3}
dict_dumped = json.dumps(dict_dataset, ensure_ascii=False)
main(amount=None, dataset = dict_dumped, path_to_save=None, output_name=None) """

 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a word cloud from the top N terms.')
    parser.add_argument('--amount', type=int, help='The number of terms to include in the word cloud.')
    parser.add_argument('--dataset', type=str, help='The dataset to use for the word cloud.')
    parser.add_argument('--path_to_save', required=True, type=str, help='The path to save the word cloud.')
    parser.add_argument('--output_name', required=True, type=str, help='The name of the output file.')
    args = parser.parse_args()
    print(f"dataset = {args.dataset}")
    main(args.amount, args.dataset, args.path_to_save, args.output_name)