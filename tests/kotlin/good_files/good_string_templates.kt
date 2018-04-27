internal abstract class A {
    protected open val v = ""
    internal open suspend fun f(v: Any): Any = ""
    public lateinit var lv: String
    abstract tailrec fun findFixPoint(x: Double = 1.0): Double
}