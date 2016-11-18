# KEY RATE DURATION FUNCTIONS
#    Calculate key rate durations of individual bonds and/or portfolios
#     assuming yields are zero-coupon rates compounded continuously.
#    Modified to work within a pandas dataframe and dictionaries.
#
# 15 November 2016
# Anthony Gusman
#
# References:
#    Nawalkha, Soto, and Beliaeva. 2005. Interest Rate Risk Modeling: The 
#       Fixed Income Valuation Course. John Wiley & Sons, Inc. New Jersey.



import numpy as np                               # MATLAB-style functions



def krdprepare(bond,keyrates,mode='disc'):
    # Prepares bond-position object for use with krd functions.
    #  Will also be used to control keyrates for mismatched.
    if keyrates=='default':
        CF = bond["couponpayments"]
        T = (1./365)* (bond["coupondates"] - bond["createdate"])
        Y = annI(bond["interestrate"],mode=mode)
        if type(Y)==float:
            Y = Y * np.ones(CF.size)
        return T, CF, Y
   
    
    
def annI(effY,n=365,mode='disc'):
    # !! KRD computation requires annualized effective rates.
    if mode=='disc':
        annY = n*((1+effY)**(1./n) - 1)
    elif mode=='cont':
        annY = effY
    return annY
#######################################0#######################################

 # GATEWAY FUNCTION   
def krdbond(bond,keyrates='default',mode='disc'):
#   Computes key rate durations of cash flows.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N
    T, CF, Y = krdprepare(bond,keyrates,mode)    
    P = pvalcf(T,CF,Y,mode)
    if mode=='cont':
        KRD = 1/P * CF*T/np.exp(Y*T)
    elif mode=='disc':
        n = 365
        KRD = 1/P * CF*T/((1+Y/n)**(n*T+1))
    return KRD

    
     
def pvalcf(T,CF,Y,mode='disc'):
#   Computes present value of cash flows.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N
    if mode=='cont':
        s = CF/np.exp(Y*T)
        P = np.sum(s)
    elif mode=='disc':
        n = 365
        s = CF/((1+Y/n)**(n*T))
        P = np.sum(s)
    return P
#######################################1#######################################


def krdport(portfolio,keyrates='default'):
#   Computes key rate duration of portfolio. Requires input bonds to have same 
#    payment length (i.e., padding with zeros). This requirement will be
#    handled by krdprepare.py
    BONDS = portfolio.to_dict('records')
    b = len(BONDS)
    KRD = [];                            W = []
    for bond in BONDS:
        KRD = np.append(KRD,krdbond(bond));  W = np.append(W,bond["weight"])
    KRD = KRD.reshape(b,len(KRD)/b)
    S = W*np.transpose(KRD)
    KRDport = np.sum(S,1)
    return KRDport
    
    

#######################################2#######################################










