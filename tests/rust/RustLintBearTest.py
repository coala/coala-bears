from bears.rust.RustLintBear import RustLintBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
fn main() {
    let s: String = "hello world".to_string();
    let s_slice: &str = &s;
    println!("{} {}", s, s_slice); // hello world hello world
}
"""

bad_file = """
fn main() {
    let s: String = "hello world".to_string();
    let s_slice: &str = &s;
}
"""

RustLintBear = verify_local_bear(RustLintBear,
                                 valid_files=(good_file,),
                                 invalid_files=(bad_file,))
