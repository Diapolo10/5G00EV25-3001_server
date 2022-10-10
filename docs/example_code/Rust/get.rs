use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {

    let url = "/";

    let response = reqwest::blocking::get(&url)?.text()?;
    println!("{:#?}", resp);
    Ok(())
}
