{ nixpkgs ? import <nixpkgs> {} }:

with nixpkgs;
stdenv.mkDerivation {
  name = "mot-0.1";
  buildInputs = [ pygame ];
}
