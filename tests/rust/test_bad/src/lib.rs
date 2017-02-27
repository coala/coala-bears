// This function should trigger unused code (warning level)
fn testssss() {
    // This comparison should trigger a `deny` level lint
    let mut x: f64 = 0.0;
    if x == std::f64::NAN {
    }
    x += 1.; // Triggers allow style lint
    println!("{}", x);
}


// We test whether bad code is found in (unit) tests
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let x = Some(1u8);
        // This match triggers a `warning` level lint
        match x {
            Some(y) => println!("{:?}", y),
            _ => ()
        }
    }
}
