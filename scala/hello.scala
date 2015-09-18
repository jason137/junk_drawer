// https://projecteuler.net

object Ciao extends App {
    println("ciao mundo!")
}

object Euler1 extends App {
    val vals = 1 until 1000     // exclusive (note "to" is inclusive)
    println(vals filter(k => k % 3 == 0 || k % 5 == 0) sum)
}

object Euler2 extends App {
    val fibs: Stream[Int] = 1 #:: 2 #:: fibs.zip(fibs.tail).map(n => n._1 + n._2)
    println(fibs takeWhile (_ < 4000000) filter (k => k % 2 == 0) sum)
}

object Euclid extends App {
    val primes: Stream[Int] = 2 #:: Stream.from(3).filter (
        i => primes.takeWhile (j => j * j <= i) forall (i % _ > 0)
    );

    def gcd(a: Int, b: Int) : Int = {
        if b == 0
            a
        else
            gcd(b, a % b)
}
