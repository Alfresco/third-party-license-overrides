# third-party-license-overrides

Centralised overrides for licenses of third party libraries used in Alfresco software.  By centralising this informaton
then corrections to license information can benefit all projects.

Currently the project is designed to be used with the [license-maven-plugin](https://www.mojohaus.org/license-maven-plugin/).

---
**Note that this project is public to allow it to be easily accessed from local and CI builds.**

---

# Licence allow list

The `includeLicenses.txt` file is a centralized list of licences allowed for use in Alfresco software. The format
of the file is one license per line, and they should be arranged in alphabetical order for ease of maintenance.

In future we may need more than one of these files as e.g. GPL licenses are allowed in certain products, provided
we have had legal approval.

# Licences merging

The `licenseMerges.txt` file contains the canonical form for various licenses. Where possible we have used the
[SPDX short identifier](https://spdx.org/licenses/) as the canonical form. The names for licenses are given in a
`|`-separated list, with the canonical form at the start of the list. The licenses should be sorted alphabetically by
canonical form. For example:

```
CPL-1.0|CPL|Common Public License
```

# License overrides

The `override-THIRD-PARTY.properties` file contains corrections to the automatically identified licenses where the
plugin has made a mistake. The format of this file is:

```
# URL to evidence for license choice
[groupId]--[artifactId]--[version]=[licenseChoice]
```

For example:

```
# https://sourceforge.net/projects/acegisecurity/
org.acegisecurity--acegi-security--0.8.2_patched=Apache-2.0
```

If multiple licenses are available for a third party library then only a single library should be included in this file
conforming to the preferences here:
https://alfresco.atlassian.net/wiki/spaces/TECH/pages/248284005/Open+Source+Licenses+-+Approval+Matrix

The libraries should be sorted alphabetically to make it easy to find them. Where possible the SPDX short identifier
should be used for the license.

# Usage

Example configuration for this will look like:

```
  <properties>
    <license-maven-plugin.version>2.0.1.alfresco-1</license-maven-plugin.version>
    ...
  </properties>
...
      <plugins>
        <plugin>
          <groupId>org.codehaus.mojo</groupId>
          <artifactId>license-maven-plugin</artifactId>
          <version>${license-maven-plugin.version}</version>
          <executions>
            <execution>
              <id>third-party-licenses</id>
              <goals>
                <goal>add-third-party</goal>
              </goals>
              <phase>generate-resources</phase>
              <configuration>
                <failOnMissing>true</failOnMissing>
                <excludedScopes>provided,test</excludedScopes>
                <excludedGroups>org.alfresco</excludedGroups>
                <failIfWarning>true</failIfWarning>
                <includedLicenses>https://raw.githubusercontent.com/Alfresco/third-party-license-overrides/master/includedLicenses.txt</includedLicenses>
                <licenseMergesUrl>https://raw.githubusercontent.com/Alfresco/third-party-license-overrides/master/licenseMerges.txt</licenseMergesUrl>
                <overrideUrl>https://raw.githubusercontent.com/Alfresco/third-party-license-overrides/master/override-THIRD-PARTY.properties</overrideUrl>
              </configuration>
            </execution>
          </executions>
        </plugin>
      </plugins>
```

In particular note the reference to this project in the `overrideUrl` tag.

To download the plugin then it may be necessary to also add the Alfresco plugin repository:

```
  <pluginRepositories>
    <pluginRepository>
      <id>alfresco-internal-plugin</id>
      <name>Alfresco Internal Repository</name>
      <url>https://artifacts.alfresco.com/nexus/content/groups/public</url>
    </pluginRepository>
  </pluginRepositories>
```

In order to also use the plugin to enforce the Alfrecso license header has been added to the top of Java files then a second execution and a dependency can be included:

```
...
            <execution>
              <id>check-licenses</id>
              <phase>compile</phase>
              <goals>
                <goal>check-file-header</goal>
              </goals>
              <configuration>
                <addJavaLicenseAfterPackage>false</addJavaLicenseAfterPackage>
                <organizationName>Alfresco Software Limited</organizationName>
                <failOnMissingHeader>true</failOnMissingHeader>
                <failOnNotUptodateHeader>true</failOnNotUptodateHeader>
                <licenseResolver>classpath://alfresco</licenseResolver>
                <licenseName>${licenseName}</licenseName>
                <roots>
                  <root>src</root>
                </roots>
                <includes>
                  <include>**/*.java</include>
                  <include>**/*.jsp</include>
                </includes>
              </configuration>
            </execution>
          </executions>
          <dependencies>
            <dependency>
              <groupId>org.alfresco</groupId>
              <artifactId>alfresco-license-headers</artifactId>
              <version>1.0</version>
            </dependency>
          </dependencies>
...
```

# Automated license file ordering

The script `licenceSorter.py` will automatically sort the three configuration files in this repository. This will make
it easier to find libraries and to check for consistency between different versions of the same library. The same
script will be run as part of the build and the build will fail if a file is not sorted correctly.

This project uses [pre-commit](https://pre-commit.com/) to automatically run the sorting script before commits. To
install pre-commit on your system see the [instructions here](https://pre-commit.com/#installation). Once you have
pre-commit installed then you can enable it for this repository by running the following command in your local clone:

```pre-commit install```

# CSV Generation for Customer Releases

We provide customers with third party license information in CSV format (or sometimes xls). To convert the THIRD-PARTY.txt files
into CSV files then this project includes a Python utility.  This can be used with a command like:

```
./thirdPartyLicenseCSVCreator.py --version 3.0.0 --project ~/projects/alfresco-elasticsearch-connector/
```

More detailed help information can be obtained with:

```
./thirdPartyLicenseCSVCreator.py --help
```
