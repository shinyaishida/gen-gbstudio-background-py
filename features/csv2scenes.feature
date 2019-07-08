Feature: Generate a set of scene image files

  Scenario Outline: Generate scene PNG files with a CSV file
    Given we have a scene "<grid>" file in CSV
    And we have a "<config>" file in JSON
    When we run the generator
    Then we get a series of PNG files like those in "<image_directory>"

  Examples:
    | grid                     | config            | image_directory             |
    | sample/scene-256x256.csv | sample/scene.json | sample/output/scene-256x256 |
    | sample/scene-256x512.csv | sample/scene.json | sample/output/scene-256x512 |
    | sample/scene-512x256.csv | sample/scene.json | sample/output/scene-512x256 |
    | sample/scene-512x512.csv | sample/scene.json | sample/output/scene-512x512 |
