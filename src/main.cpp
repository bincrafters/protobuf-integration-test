#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>

#include "addressbook.pb.h"

TEST_CASE( "Person can be serialized", "[serialization]" ) {
    tutorial::Person person;

    person.set_id(21);
	person.set_name("Bincrafters");
	person.set_email("bincrafters@github.com");

    const std::string person_string{person.SerializeAsString()};
    std::cout << "Serialized Person: " << person_string << std::endl;

    tutorial::Person recovered_person;
    REQUIRE ( recovered_person.ParseFromString(person_string) );
    REQUIRE ( recovered_person.id() == person.id() );
    REQUIRE ( recovered_person.name() == person.name() );
    REQUIRE ( recovered_person.email() == person.email() );
}
