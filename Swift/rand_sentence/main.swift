import Foundation

/*
func readOneLine() -> String {

    var result = String()
    var c = getchar()

    while c != EOF && c != 10 {
        result.append(UnicodeScalar(UInt32(c)))
        c = getchar()
    }

    return result
}
*/

func main() {
    
    var sentences = [String]()
    var oneSentense = readLine()

    while oneSentense != nil {
        sentences.append(oneSentense!)
        oneSentense = readLine()
    }
    let index = Int(arc4random_uniform(UInt32(sentences.count)))

    if sentences.count > 0 {
        print(sentences[index])
    } else {
        print("")
    }
}

main()
