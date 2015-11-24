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
    "We are twice armed if we fight with faith. -- Plato",
    "Everything that is done in the world is done by hope. -- Martin Luther",
    "Young man, in mathematics you don't understand things. You just get used to them. -- John von Neumann",
    "In most sciences one generation tears down what another has built and what one has established another undoes. In mathematics alone each generations adds a new story to the old structure. -- Hermann Hankel"
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
