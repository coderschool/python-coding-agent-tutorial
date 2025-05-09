package main

import "fmt"

func fizzbuzz(n int) {
    for i := 1; i <= n; i++ {
        switch {
        case i%15 == 0:
            fmt.Println("FizzBuzz")
        case i%3 == 0:
            fmt.Println("Fizz")
        case i%5 == 0:
            fmt.Println("Buzz")
        default:
            fmt.Println(i)
        }
    }
}

func main() {
    // Execute FizzBuzz for numbers 1 to 15
    fizzbuzz(15)
}