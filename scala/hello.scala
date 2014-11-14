// https://projecteuler.net

object ciao extends App {
    println("ciao mundo!")
}

object euler1 extends App {
    val vals = 1 until 1000     // exclusive (note "to" is inclusive)
    println(vals filter(k => k % 3 == 0 || k % 5 == 0) sum)
}

object euler2 extends App {
    val fibs: Stream[Int] = 1 #:: 2 #:: fibs.zip(fibs.tail).map(n => n._1 + n._2)
    println(fibs takeWhile (_ < 4000000) filter(k => k % 2 == 0) sum)
}

object euler3 extends App {
    val primes: Stream[Int] = 2 #:: Stream.from(3).filter(i =>
        primes.takeWhile{j => j * j <= i}.forall{ k => i % k > 0});

    primes take 10 foreach println
}
