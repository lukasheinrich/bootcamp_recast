import pyhf
import json
import click

@click.command()
@click.argument('data')
@click.argument('background')
@click.argument('signal')
@click.option('-o','--outputfile',default = 'fitresult.json')
def main(data,background,signal,outputfile):
    data = json.load(open(data))
    background = json.load(open(background))
    signal = json.load(open(signal))

    # build likelihood

    pdf = pyhf.simplemodels.hepdata_like(
        signal['counts'],
        background['counts'],
        background['uncert'],
    )
    obs,expset = pyhf.utils.hypotest(
        1.0,
        data['counts'] + pdf.config.auxdata,
        pdf,
        return_expected_set = True
    )
    result = {
        'obs': obs.tolist()[0],
        'exp': [e.tolist()[0] for e in expset]
    } 
    result = json.dumps(result, indent = 4)
    click.secho(result)
    with open(outputfile,'w') as f:
        f.write(result)


if __name__ == '__main__':
    main()