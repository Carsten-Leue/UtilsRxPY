def buildInfo = bzSemantic(
        useAnalysisSonarQube: false,
        verbose: false,
        native: [
                kind    : 'python-package',
                contacts: [
                        "": [
                                moniker: "Carsten-Leue",
                                github : "TODO",
                                slack  : "TODO",
                                roles  : ["notify", "owner"]
                        ]
                ],
                docker  : false
        ]
)