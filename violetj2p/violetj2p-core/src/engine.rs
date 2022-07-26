/// Contains lowlevel functions for accepting environement JSON data,
/// converting it to a model, and embedding it into an HTML rowcol schema.
use super::*;
use model::event::Event;

/// Parses command line arguments into a Vec<Event>
pub fn parse_deps(args: Vec<String>) -> Result<Vec<Event>, anyhow::Error> {
    let mut deps: Vec<Event> = vec![];
    for s in args.iter() {
        // Here, our TryFrom<String> implementations for the Event type attempts
        // to deserialize the command-line passed json String into a model::Event.
        let e = Event::try_from(s.to_string())?;
        deps.push(e);
    }
    Ok(deps)
}

/// Generates a HTML representation from a Vec<Event>
///     MOCK IMPLEMENTATION
///
/// - Will need to have knowledge of our defined schema to
///   generate the event-embedded HTML.
///
/// - The algorithm relies on the HTML schema to be built as components,
///   i.e. rowcol components, and header/footer components, and works as so:
/// - 1. A workaround to not knowing how many events we'll have to handle at runtime
///      is to simply loop through them and generate a rowcol component for each.
///      This is done by simply mapping each event's fields to the columns we've already defined
///      for our statements
/// - 2. Header/footer components are then appended to the rowcol components.
/// - 3. The algorithm returns a fully-formed HTML statement as Ok(String)     
pub fn make_html(deps: Vec<Event>) -> Result<String, anyhow::Error> {
    Ok(String::new())     
}