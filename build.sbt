name := "play-java-intro"

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayJava)

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  // If you enable PlayEbean plugin you must remove these
  // JPA dependencies to avoid conflicts.
  javaJpa,
  "org.hibernate" % "hibernate-entitymanager" % "4.3.7.Final",
  "org.scribe" % "scribe" % "1.3.7",
  "org.dom4j" % "dom4j" % "2.0.0-RC1",
  "com.googlecode.json-simple" % "json-simple" % "1.1.1"
)

libraryDependencies ++= Seq(
  "com.amazonaws" % "aws-java-sdk" % "1.11.46"
)

