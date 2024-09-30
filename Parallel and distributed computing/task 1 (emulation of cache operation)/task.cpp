#include <list>
#include <vector>
#include <iostream>
#include <algorithm>
#include <unordered_map>

class Cache
{
public:
    Cache(int capacity)
        : m_Capacity(capacity)
    {
    }

    bool Get(int key)
    {
        if (m_CacheMap.find(key) != m_CacheMap.end())
        {
            m_CacheList.splice(m_CacheList.begin(), m_CacheList, m_CacheMap[key]);
            m_CacheMap[key] = m_CacheList.begin();
            return true;
        }
        return false;
    }

    void Put(int key)
    {
        if (m_CacheMap.find(key) != m_CacheMap.end())
        {
            m_CacheList.splice(m_CacheList.begin(), m_CacheList, m_CacheMap[key]);
        }
        else
        {
            if (m_CacheList.size() == m_Capacity)
            {
                int LeastUsed = m_CacheList.back();
                m_CacheList.pop_back();
                m_CacheMap.erase(LeastUsed);
            }
            m_CacheList.push_front(key);
        }
        m_CacheMap[key] = m_CacheList.begin();
    }

private:
    int                                               m_Capacity;
    std::list<int>                                    m_CacheList;
    std::unordered_map<int, std::list<int>::iterator> m_CacheMap;
};

class CacheWork
{
public:
    CacheWork() = default;

    friend std::istream& operator >> (std::istream& in, CacheWork& a)
    {
        in >> a.m_CacheSize >> a.m_Associativity >> a.m_LineSize >> a.m_Size;
        a.m_Addresses.resize(a.m_Size);
        for (int i = 0; i < a.m_Size; ++i)
        {
            in >> a.m_Addresses[i];
        }
        return in;
    }

    void Solution()
    {
        int CacheHits = 0, CacheMisses = 0;
        int NumSets = m_CacheSize / (m_Associativity * m_LineSize);
        std::vector<Cache> cache_sets(NumSets, Cache(m_Associativity));

        for (auto address : m_Addresses)
        {
            int L = address / m_LineSize;
            int N = L % NumSets;

            if (cache_sets[N].Get(L))
            {
                ++CacheHits;
            }
            else
            {
                ++CacheMisses;
                cache_sets[N].Put(L);
            }
        }

        std::cout << CacheHits << " " << CacheMisses << "\n";
    }

private:
    int              m_Size;
    int              m_CacheSize;
    int              m_Associativity;
    int              m_LineSize;
    std::vector<int> m_Addresses;
};

int main()
{
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
    std::ios_base::sync_with_stdio(0);
    std::cin.tie(0);
    std::cout.tie(0);
    CacheWork a;
    std::cin >> a;
    a.Solution();
    return 0;
}
