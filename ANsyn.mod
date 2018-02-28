COMMENT
A synaptic current with two dual exponential function conductances,
representing non-voltage-dependent AMPA and voltage-dependent NMDA
components.  The basic dual exponential conductance is given by:
         g = 0 for t < onset and
         g = gmax*((tau1*tau2)/(tau1-tau2)) *
                             (exp(-(t-onset)/tau1)-exp(-(t-onset)/tau2))
         for t > onset (tau1 and tau2 are fast and slow time constants)
The synaptic current is:
        i = (gA + gN) * (v - e)      i(nanoamps), g(micromhos);
NMDA model taken from Mel, J. Neurophys. 70:1086-1101, 1993
BPG 1-12-00
ENDCOMMENT
                           
INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
    POINT_PROCESS ANSynapse
    RANGE onset, gmax, e, i, g, gA, gN, tau1, tau2, Ntau1, Ntau2, eta, Mg, gamma, Nfrac
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (umho) = (micromho)
}

PARAMETER {
    onset=0 (ms)
    tau1=.2 (ms)    <1e-3,1e6>
    tau2=2 (ms)    <1e-3,1e6>
    Nfrac=0.5
    Ntau1=.66 (ms)    <1e-3,1e6>
    Ntau2=80 (ms)    <1e-3,1e6>
    eta=0.33 (/mM)
    Mg=1 (mM)
    gamma=0.06 (/mV)
    gmax=0  (umho)  <0,1e9>
    e=0 (mV)
    v   (mV)
}

ASSIGNED { i (nA)  g (umho) gA (umho) gN (umho) Agmax (umho) Ngmax (umho)}

INITIAL {
    Agmax = (1-Nfrac)*gmax
    Ngmax = Nfrac*gmax
}

BREAKPOINT {
    gA = Agmax*((tau1*tau2)/(tau1-tau2))*duale((t-onset)/tau1,(t-onset)/tau2)
    gN = Ngmax*((Ntau1*Ntau2)/(Ntau1-Ntau2))*duale((t-onset)/Ntau1,(t-onset)/Ntau2)
    gN = gN / (1 + (eta*Mg*exp(-gamma*v)))
    g = gA + gN
    i = g*(v - e)
}

FUNCTION duale(x,y) {
    if (x < 0 || y < 0) {
        duale = 0
    }else{
        duale = exp(-x) - exp(-y)
    }
}
