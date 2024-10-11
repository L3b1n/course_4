#include <vector>
#include <iostream>

constexpr int       BLOCK_SIZE = 8;
constexpr long long MOD = 987654321054321LL;
constexpr long long MUL = 179;

class Matrix
{
public:
    Matrix()
    {
    }

    void Solution()
    {
        std::cin >> m_Size >> m_Seed >> m_Count;

        m_Input.resize(m_Size * m_Size);
        for (size_t i = 0; i < m_Input.size(); ++i)
        {
            m_Input[i] = m_Seed;
            m_Seed = ((long long) m_Seed * 197 + 2017) & 987654;
        }

        for (int i = 0; i < m_Count; ++i)
        {
            int MinI, MinJ, Size;
            std::cin >> MinI >> MinJ >> Size;
            TransposeSubmatrix(MinI, MinJ, Size);
        }

        long long ResultValue = 0;
        for (size_t i = 0; i < m_Input.size(); ++i)
        {
            ResultValue = (ResultValue * MUL + m_Input[i]) & MOD;
        }

        std::cout << ResultValue << "\n";
    }

private:
    void TransposeSubmatrix(
        int imin,
        int jmin,
        int size)
    {
        for (int i = 0; i < size; i += BLOCK_SIZE)
        {
            for (int j = 0; j < size; j += BLOCK_SIZE)
            {
                int MaxI = std::min(i + BLOCK_SIZE, size);
                int MaxJ = std::min(j + BLOCK_SIZE, size);
                
                for (int bi = i; bi < MaxI; ++bi)
                {
                    for (int bj = j; bj < MaxJ; ++bj)
                    {
                        if (bi < bj)
                        {
                            int idx1 = (imin + bi) * m_Size + (jmin + bj);
                            int idx2 = (imin + bj) * m_Size + (jmin + bi);
                            std::swap(m_Input[idx1], m_Input[idx2]);
                        }
                    }
                }
            }
        }
    }

private:
    int              m_Size;
    int              m_Seed;
    int              m_Count;
    std::vector<int> m_Input;
};

int main()
{
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
    std::ios_base::sync_with_stdio(0);
    std::cin.tie(0);
    std::cout.tie(0);
    Matrix a;
    a.Solution();
    return 0;
}
