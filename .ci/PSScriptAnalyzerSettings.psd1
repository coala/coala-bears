@{
    Severity = @('Error', 'Warning')

    IncludeDefaultRules = $true

    # List all rules here, otherwise they are excluded.
    # Some are inactive because they need to be configured before usable.

    IncludeRules = @(
        'PSAlignAssignmentStatement'
        'PSAvoidAlias'
        'PSAvoidAssignmentToAutomaticVariable'
        'PSAvoidDefaultTrueValueSwitchParameter'
        'PSAvoidDefaultValueForMandatoryParameter'
        'PSAvoidEmptyCatchBlock'
        'PSAvoidGlobalAliases'
        'PSAvoidGlobalFunctions'
        'PSAvoidGlobalVars'
        'PSAvoidInvokingEmptyMembers'
        'PSAvoidNullOrEmptyHelpMessageAttribute'
        'PSAvoidPositionalParameters'
        'PSAvoidReservedCharInCmdlet'
        'PSAvoidReservedParams'
        'PSAvoidShouldContinueWithoutForce'
        'PSAvoidTrailingWhitespace'
        'PSAvoidUserNameAndPasswordParams'
        'PSAvoidUsingComputerNameHardcoded'
        'PSAvoidUsingConvertToSecureStringWithPlainText'
        'PSAvoidUsingDeprecatedManifestFields'
        'PSAvoidUsingInvokeExpression'
        'PSAvoidUsingPlainTextForPassword'
        'PSAvoidUsingWMICmdlet'
        # Easier to use inside Fudge
        # 'PSAvoidUsingWriteHost'
        'PSDscExamplesPresent'
        'PSDscTestsPresent'
        'PSMisleadingBacktick'
        'PSMissingModuleManifestField'
        'PSPlaceCloseBrace'
        'PSPlaceOpenBrace'
        'PSPossibleIncorrectComparisonWithNull'
        'PSPossibleIncorrectUsageOfAssignmentOperator'
        'PSPossibleIncorrectUsageOfRedirectionOperator'
        'PSProvideCommentHelp'
        'PSReturnCorrectTypesForDSCFunctions'
        'PSUseApprovedVerbs'
        # Not suitable for other OS
        # 'PSUseBOMForUnicodeEncodedFile'
        'PSUseCmdletCorrectly'
        'PSUseCompatibleCmdlets'
        'PSUseConsistentIndentation'
        'PSUseConsistentWhitespace'
        'PSUseCorrectCasing'
        'PSUseDeclaredVarsMoreThanAssignments'
        'PSUseIdenticalMandatoryParametersDSC'
        'PSUseIdenticalParametersDSC'
        'PSUseLiteralInitializerForHashtable'
        'PSUseOutputTypeCorrectly'
        'PSUsePSCredentialType'
        'PSUseShouldProcessCorrectly'
        'PSUseShouldProcessForStateChangingFunctions'
        'PSUseSingularNouns'
        'PSUseStandardDSCFunctionsInResource'
        'PSUseSupportsShouldProcess'
        'PSUseToExportFieldsInManifest'
        'PSUseUTF8EncodingForHelpFile'
        'PSUseVerboseMessageInDSCResource'
        # Compatibility subdirectory
        'PSUseCompatibleCommands'
        'PSUseCompatibleSyntax'
        'PSUseCompatibleTypes'
    )

    # The Rules here are mostly manually imported from
    # https://github.com/PowerShell/PSScriptAnalyzer/blob/master/Engine/Settings/CodeFormatting.psd1
    # except `PSUseConsistentWhitespace.CheckOperator` is disabled as incompatible
    # https://github.com/PowerShell/PSScriptAnalyzer/issues/769

    Rules = @{
        PSPlaceOpenBrace = @{
            Enable = $true
            OnSameLine = $true
            NewLineAfter = $true
            IgnoreOneLineBlock = $true
        }

        PSPlaceCloseBrace = @{
            Enable = $true
            NewLineAfter = $true
            IgnoreOneLineBlock = $true
            NoEmptyLineBefore = $false
        }

        PSUseConsistentIndentation = @{
            Enable = $true
            Kind = 'space'
            PipelineIndentation = 'IncreaseIndentationForFirstPipeline'
            IndentationSize = 4
        }

        PSUseConsistentWhitespace = @{
            Enable = $true
            CheckInnerBrace = $true
            CheckOpenBrace = $true
            CheckOpenParen = $true
            CheckOperator = $true
            CheckPipe = $true
            CheckSeparator = $true
        }

        PSAlignAssignmentStatement = @{
            Enable = $true
            CheckHashtable = $false
        }

        PSUseCorrectCasing = @{
            Enable = $true
        }
    }
}
