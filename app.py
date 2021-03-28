from flask import Flask, render_template, request
import itertools
from collections import Counter
import re
import pandas as pd
app = Flask(__name__)


def genes_combinations(F_genotype, M_genotype):
    # combine every gene of Father with Mother
    print(F_genotype, M_genotype)

    possible_genes = []
    for i in range(0, len(F_genotype) - 1, 2):
        genes = itertools.product(F_genotype[i:i + 2], M_genotype[i:i + 2])
        possible_genes.append(genes)

    return possible_genes


def genotypes_combinations(all_genes):
    all_genotypes = list(itertools.product(*all_genes))

    # print(len(all_genotypes)) number of possible genotypes = 4096

    summary_genotypes = dict(Counter(all_genotypes))
    genotypes = dict()

    for key, values in summary_genotypes.items():
        new_key = ""
        for gene in key:
            if gene[0] > gene[1]: gene = (gene[1],gene[0])
            new_key += ''.join(gene)
        if new_key in genotypes: genotypes[new_key] += values
        else: genotypes[new_key] = values

    return genotypes

phenotypes = {'Golden Agouti': r'A.C.D.E.G.P.',
                'Grey Agouti': r'A.C.D.E.ggP.',
                'Argente Golden': r'A.CCD.E.G.pp',
                'Argente Cream': r'A.CchD.E.G.pp',
                'Cream (Ivory cream)': r'A.C.D.E.ggpp',
                'Dark Eyed Honey': r'A.C.D.eeG.P.',
                'Yellow Fox (Red Eyed Honey)': r'A.C.D.eeG.pp',
                'Nutmeg': r'aaC.D.eeG.P.',
                'Silver Nutmeg': r'aaC.D.eeggP.',
                'Saffron (Red Fox - Argente Nutmeg)': r'aaC.D.eeG.pp',
                'Black': r'aaC.D.E.G.P.',
                'Pearl (Colourpoint Agouti)': r'A.cbc.D.E.G.P.',
                'Slate': r'aaC.D.E.ggP.',
                'Lilac': r'aaCCD.E.G.pp',
                'Dove': r'aaCchD.E.G.pp',
                'Ruby Eyed White (REW)*': r'aaC.D.E.ggpp',
                'Burmese': r'aacbcbD.E.G.P.',
                'Siamese': r'aacbchD.E.G.P.',
                'Pink Eyed White (PEW)*': r'..chchD.E...pp',
                'Dark Tailed White/Himalayan (DTW)*': r'..chchD.E...P.',
                'Black Eyed White*': r'..cbchD.eeggP.'}

def possible_phenotypes(all_genotypes):
    result = dict()
    print(all_genotypes)
    for key, value in all_genotypes.items():
        for key_p, value_p in phenotypes.items():
            #print(value_p, key)
            if re.match(value_p,key):
                if key_p in result.keys():
                    result[key_p] += value
                else:
                    result[key_p] = value

    return result






@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        #father's genotype
        F_genotype = request.form.getlist('F_genotype[]')
        M_genotype = request.form.getlist('M_genotype[]')

        all_genes = genes_combinations(F_genotype, M_genotype)
        all_genotypes = genotypes_combinations(all_genes)
        result = possible_phenotypes(all_genotypes)

        df = pd.DataFrame.from_dict(result, orient='index',columns=["Quantity"])
        df["%"] = df["Quantity"] / 4096 * 100
        dfhtml = df.to_html()

        return render_template('app2.html', result = dfhtml)

    return render_template('app.html')

if __name__=='__main__':
    app.run(debug=True)