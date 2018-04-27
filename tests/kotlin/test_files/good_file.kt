fun test() {
  listOf(1, 2, 3)
    .map {
      it.toString()
    }
    .filter {
      it.isNotBlank()
    }
    .map { "alsdfjadsf" }
    .map { "adsjfhasdf" }
}