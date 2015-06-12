#include <stdio.h>
#include <stdlib.h>
#include <time.h>

char *sentences[] = {
    "If you want to go fast, go alone. If you want to go far, go together.",
    "It is the tears of the earth that keep her smiles in bloom. -- Rabindranath Tagore",
    "Be the change that you wish to see in the world. -- Mahatma Gandhi",
    "If you tell the truth, you don't have to remember anything. -- Mark Twain",
    "Live as if you were to die tomorrow. Learn as if you were to live forever. -- Mahatma Gandhi",
    "Order and simplification are the first steps toward the mastery of a subject. -- Thomas Mann",
    "We are twice armed if we fight with faith. -- Plato"
};

int main()
{
    srand(time(NULL));
    int r = rand();
    int l = sizeof(sentences) / sizeof(sentences[0]);
    char *msg = sentences[r % l];
    printf("%s\n", msg);
    return 0;
}
