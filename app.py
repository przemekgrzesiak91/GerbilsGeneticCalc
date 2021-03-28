from flask import Flask, render_template, request
import itertools
from collections import Counter

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
    return summary_genotypes



@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        #father's genotype
        F_genotype = request.form.getlist('F_genotype[]')
        M_genotype = request.form.getlist('M_genotype[]')

        all_genes = genes_combinations(F_genotype, M_genotype)
        all_genotypes = genotypes_combinations(all_genes)
        return render_template('app2.html', result = all_genotypes)

    return render_template('app.html')

if __name__=='__main__':
    app.run(debug=True)