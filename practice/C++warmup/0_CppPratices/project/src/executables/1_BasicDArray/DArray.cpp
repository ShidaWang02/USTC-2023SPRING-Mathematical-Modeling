// implementation of class DArray
#include <iostream>

#include "DArray.h"

#include <cassert>

using namespace std;

// default constructor
DArray::DArray()
{
	Init();
}

// set an array with default values
DArray::DArray(int nSize, double dValue)
{
	// TODO
	m_pData = new double[nSize];
	m_nSize = nSize;
	for (int i = 0; i < nSize; i++)
	{
		m_pData[i] = dValue;
	}
}

DArray::DArray(const DArray &arr)
{
	// TODO
	m_pData = new double[arr.m_nSize];
	m_nSize = arr.m_nSize;
	for (int i = 0; i < m_nSize; i++)
	{
		m_pData[i] = arr.m_pData[i];
	}
}

// deconstructor
DArray::~DArray()
{
	Free();
}

// display the elements of the array
void DArray::Print() const
{
	// TODO
	cout << "size = " << m_nSize << ":";
	for (int i = 0; i < GetSize(); i++)
		cout << " " << GetAt(i);

	cout << endl;
}

// initilize the array
void DArray::Init()
{
	// TODO
	m_pData = nullptr;
	m_nSize = 0;
}

// free the array
void DArray::Free()
{
	// TODO
	delete[] m_pData;
	m_pData = nullptr;
	m_nSize = 0;
}

// get the size of the array
int DArray::GetSize() const
{
	// TODO
	return m_nSize; // you should return a correct value
}

// set the size of the array
void DArray::SetSize(int nSize)
{
	// TODO
	if (m_nSize == nSize)
	{
		return;
	}
	double *pCopyData = new double[nSize];
	int copyNum = nSize < m_nSize ? nSize : m_nSize;
	for (int i = 0; i < copyNum; i++)
	{
		pCopyData[i] = m_pData[i];
	}
	for (int i = copyNum; i < nSize; i++)
	{
		pCopyData[i] = 0;
	}
	delete[] m_pData;
	m_pData = pCopyData;
	m_nSize = nSize;
}

// get an element at an index
const double &DArray::GetAt(int nIndex) const
{
	// TODO
	assert(nIndex >= 0 && nIndex < m_nSize);
	return m_pData[nIndex];
}

// set the value of an element
void DArray::SetAt(int nIndex, double dValue)
{
	// TODO
	assert(nIndex >= 0 && nIndex < m_nSize);
	m_pData[nIndex] = dValue;
}

// overload operator '[]'
const double &DArray::operator[](int nIndex) const
{
	// TODO
	assert(nIndex >= 0 && nIndex < m_nSize);
	return m_pData[nIndex];
}

// add a new element at the end of the array
void DArray::PushBack(double dValue)
{
	// TODO
	double* pTemp = new double[m_nSize + 1];

	for (int i = 0; i < m_nSize; i++)
		pTemp[i] = m_pData[i];

	pTemp[m_nSize] = dValue;

	delete[] m_pData;
	m_pData = pTemp;
	m_nSize++;
}

// delete an element at some index
void DArray::DeleteAt(int nIndex)
{
	// TODO
	assert(nIndex >= 0 && nIndex < m_nSize);

	double *pCopy = new double[m_nSize - 1];
	for (int i = 0; i < nIndex; i++)
	{
		pCopy[i] = m_pData[i];
	}
	for (int i = nIndex; i < m_nSize - 1; i++)
	{
		pCopy[i] = m_pData[i + 1];
	}
	delete[] m_pData;
	m_pData = pCopy;
	m_nSize -= 1;
}

// insert a new element at some index
void DArray::InsertAt(int nIndex, double dValue)
{
	// TODO
	assert(nIndex >= 0 && nIndex <= m_nSize);

	double *pCopy = new double[m_nSize + 1];
	for (int i = 0; i < nIndex; i++)
	{
		pCopy[i] = m_pData[i];
	}
	pCopy[nIndex] = dValue;
	for (int i = nIndex + 1; i < m_nSize + 1; i++)
	{
		pCopy[i] = m_pData[i - 1];
	}
	delete[] m_pData;
	m_pData = pCopy;
	m_nSize += 1;
}

// overload operator '='
DArray &DArray::operator=(const DArray &arr)
{
	// TODO
	delete[] m_pData;

	m_nSize = arr.m_nSize;
	m_pData = new double[m_nSize];

	for (int i = 0; i < m_nSize; i++)
		m_pData[i] = arr[i];
	return *this;
}
