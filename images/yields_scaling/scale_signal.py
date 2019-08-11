import numpy as np
import click
import uproot

@click.command()
@click.argument('inputfile')
@click.argument('xsec', type = float)
@click.option('--lumi',default = 1000)
@click.option('--outputfile',default = 'scaled.json')
def main(inputfile,xsec,lumi,outputfile):
    f = uproot.open(inputfile)
    s,_ = f['h_mjj_kin'].numpy()
    s = s * xsec * lumi
    rebinned_signal = [np.sum(x) for x in np.split(s,list(range(10,len(s),10)))]


    ds = {
        "counts": rebinned_signal
    }

    import json
    with open(outputfile,'w') as f:
        json.dump(ds,f, indent = 4)

if __name__ == '__main__':
    main()
