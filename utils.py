#!/usr/bin/python
#https://www.evernote.com/Home.action#st=p&n=ce6db451-ebfe-4891-ac0a-bb34b724be27

import sys

# Loan interface
#   GetOutstandingPayment()
#   GetNextMonthPayment()
#   PayForThisMonth()

def actuarial(i, n):
    return (1 - (1 + i) ** -n) / i

def PMT(i, n, M):
    if n == 0: return 0
    aI = 1 / actuarial(i, n)
    return M * aI

class MortgageLoan:
    def __init__(self, i, n, M):
        self.n_left = n
        self.current_i = i
        self.outstanding_m = M
        self.pmt = PMT(i, n, M)

    def GetOutstandingPayment(self):
        return self.outstanding_m

    # return (payment, interest)
    def GetNextMonthPayment(self):
        if self.n_left > 0:
            return (self.pmt, self.current_i * self.outstanding_m)
        else:
            return (0, 0)

    def PayForThisMonth(self):
        if self.n_left > 0:
            (total, interest) = self.GetNextMonthPayment()
            self.outstanding_m = self.outstanding_m - total + interest
            self.n_left = self.n_left - 1

    def PayTillTheEnd(self):
        total_payment = 0
        total_interest = 0
        while self.n_left > 0:
            (payment, interest) = self.GetNextMonthPayment()
            total_payment = total_payment + payment
            total_interest = total_interest + interest
            self.PayForThisMonth()
        return (total_payment, total_interest)

class NoTermLoan:
    def __init__(self, i, M):
        self.current_i = i
        self.outstanding_m = M
        self.n_passed = 0

    def GetOutstandingPayment(self):
        return self.outstanding_m * (self.n_passed * i + 1)

    def GetNextMonthPayment(self):
        return (0, 0)

    def PayForThisMonth(self):
        self.n_passed = self.n_passed + 1

# Input:
# P: present value of the investment
# n: mortgage loan term
# R: Monthly income of the investment
# M: Mortgage ammount
def GenerateCashFlowCurve(P, n, M, R):
    for I in xrange(1, 101):
        i = I / 1000. / 12.
        loan = MortgageLoan(i, n, M)
        yield I/10., R - loan.GetNextMonthPayment()[0]

# Input:
# P: present value of the investment
# i: interests rate
# n: mortgage loan term
# R: Monthly income of the investment
def GenerateInitialYieldCurve(P, n, i, R):
    for m in xrange(0, int(P * .9), 100):
        loan = MortgageLoan(i, n, m)
        (payment, interest) = loan.GetNextMonthPayment()
        cash_flow = R - payment
        negative_cash_flow = -cash_flow if cash_flow < 0 else 0
        initial_yield = (R - interest) / (P - m + negative_cash_flow) * 12. * 100
        yield m, initial_yield

# Input:
# P: present value of the investment
# i: interests rate
# n: mortgage loan term
# R: Monthly income of the investment
def GenerateTotalYieldCurve(P, n, i, R):
    for m in xrange(0, int(P * .9), 100):
        loan = MortgageLoan(i, n, m)
        (total_payment, total_interest) = loan.PayTillTheEnd()
        total_rental = R * n
        total_cash_flow = total_rental - total_payment
        negative_total_cash_flow = -total_cash_flow if total_cash_flow < 0 else 0
        total_yield = (total_rental - total_interest) / (P - m + negative_total_cash_flow) / (n / 12.) * 100
        yield m, total_yield

if __name__ == "__main__":
    CMD = sys.argv[1]

    if CMD == "PMT": # Montly mortgaage payment
        P = int(sys.argv[2])
        n = int(sys.argv[3])
        i = float(sys.argv[4]) / 100. / 12.
        print PMT(i, n, P)
    elif CMD == "TPMT": # Total mortgage payment
        P = int(sys.argv[2])
        n = int(sys.argv[3])
        i = float(sys.argv[4]) / 100. / 12.
        m = MortgageLoan(i, n, P)
        print m.PayTillTheEnd()
    elif CMD == "CFC": # Monthly cashflow curve of different rate
        P = int(sys.argv[2])
        n = int(sys.argv[3])
        M = int(sys.argv[4])
        R = float(sys.argv[5])
        for i in GenerateCashFlowCurve(P, n, M, R):
            print ' '.join(map(str, i))
    elif CMD == "IYC": # Initial Yield Curve(of different down payment)
        P = int(sys.argv[2])
        n = int(sys.argv[3])
        i = float(sys.argv[4]) / 100. / 12.
        R = float(sys.argv[5])
        for i in GenerateInitialYieldCurve(P, n, i, R):
            print ' '.join(map(str, i))
    elif CMD == "TYC": # Total Yield Curve(of different down payment)
        P = int(sys.argv[2])
        n = int(sys.argv[3])
        i = float(sys.argv[4]) / 100. / 12.
        R = float(sys.argv[5])
        for i in GenerateTotalYieldCurve(P, n, i, R):
            print ' '.join(map(str, i))
    else:
        sys.exit(1)
    sys.exit(0)
