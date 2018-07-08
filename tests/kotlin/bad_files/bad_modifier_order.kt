abstract internal class A {
    open protected val v = ""
    open suspend internal fun f(v: Any): Any = ""
    lateinit public var lv: String
    tailrec abstract fun findFixPoint(x: Double = 1.0): Double
}