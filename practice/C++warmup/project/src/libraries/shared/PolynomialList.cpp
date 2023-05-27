#include "PolynomialList.h"

#include <iostream>
#include <algorithm>
#include <fstream>
#include <cmath>
#include <assert.h>

using namespace std;

PolynomialList::PolynomialList(const PolynomialList& other) {
    // TODO
    m_Polynomial = other.m_Polynomial;
}

PolynomialList::PolynomialList(const string& file) {
    // TODO
    ReadFromFile(file);
}

PolynomialList::PolynomialList(const double* cof, const int* deg, int n) {
    // TODO
    for (int i = 0; i < n; i++)
    {
        AddOneTerm(Term(deg[i], cof[i]));
    }
}

PolynomialList::PolynomialList(const vector<int>& deg, const vector<double>& cof) {
    // TODO
    assert(deg.size() == cof.size());

    for (size_t i = 0; i < deg.size(); i++)
    {
        AddOneTerm(Term(deg[i], cof[i]));
    }
    
}

double PolynomialList::coff(int i) const {
    // TODO
    auto itr = m_Polynomial.begin();
    for (; itr != m_Polynomial.end(); itr++)
    {
        if (itr->deg > i)
        {
            break;
        }
        if (itr->deg == i)
        {
            return itr->cof;
        }
    }
    
    return 0.; // you should return a correct value
}

double& PolynomialList::coff(int i) {
    // TODO
    return AddOneTerm(Term(i,0)).cof;
}

void PolynomialList::compress() {
    // TODO
    auto itr = m_Polynomial.begin();
    for (; itr != m_Polynomial.end();)
    {
        if (fabs((*itr).cof) < 1e-6)
            m_Polynomial.erase(itr++);
        else
            itr++;
    }
    
}

PolynomialList PolynomialList::operator+(const PolynomialList& right) const {
    // TODO 
    PolynomialList poly(right);
    for (auto itr = m_Polynomial.begin(); itr != m_Polynomial.end(); itr++)
    {
        poly.AddOneTerm(*itr);
    }
    poly.compress();
    return poly; // you should return a correct value
}

PolynomialList PolynomialList::operator-(const PolynomialList& right) const {
    // TODO
    PolynomialList poly(right);
    for (auto itr = m_Polynomial.begin(); itr != m_Polynomial.end(); itr++)
    {
        poly.AddOneTerm(Term(itr->deg, -itr->cof));
    }
    poly.compress();
    return poly; // you should return a correct value
}

PolynomialList PolynomialList::operator*(const PolynomialList& right) const {
    // TODO
    PolynomialList poly;

    for (auto itr1 = m_Polynomial.begin(); itr1 != m_Polynomial.end(); itr1++)
    {
        for (auto itr2 = right.m_Polynomial.begin(); itr2 != right.m_Polynomial.end(); itr2++)
        {
            double cof = itr1->cof * itr2->cof;
            int deg = itr1->deg + itr2->deg;
            poly.AddOneTerm(Term(deg, cof));
        }
        
    }
    
    return poly; // you should return a correct value
}

PolynomialList& PolynomialList::operator=(const PolynomialList& right) {
    // TODO
    m_Polynomial = right.m_Polynomial;
    return *this;
}

void PolynomialList::Print() const {
    // TODO
    auto itr = m_Polynomial.begin();
    if (itr == m_Polynomial.end())
    {
        cout << "0" << endl;
        return;
    }
    
    for (; itr != m_Polynomial.end(); itr++)
    {
        if (itr != m_Polynomial.begin()) {
            cout << " ";
            if (itr->cof > 0)
                cout << "+";
        }

        cout << itr->cof;

        if (itr->deg > 0)
            cout << "x^" << itr->deg;
    }
    
    cout << endl;

}

bool PolynomialList::ReadFromFile(const string& file) {
    // TODO
    m_Polynomial.clear();

    ifstream infile;
    infile.open(file.c_str());
    if (!infile.is_open()) {
        cout << "Can not open [" << file << "]" << endl;
        return false;
    }
    char ch;
    int n;
    infile >> ch;
    infile >> n;
    for (int i = 0; i < n; i++) {
        Term term;
        infile >> term.deg;
        infile >> term.cof;

        AddOneTerm(term);
    }

    infile.close();
    return true; // you should return a correct value
}

PolynomialList::Term& PolynomialList::AddOneTerm(const Term& term) {
    // TODO
    auto itr = m_Polynomial.begin();
    for (; itr!= m_Polynomial.end(); itr++)
    {
        if (itr->deg == term.deg)
        {
            itr->cof += term.cof;
            return *itr;
        }
        
        if(itr->deg > term.deg)
            break;
    }
    return *m_Polynomial.insert(itr, term);
}
