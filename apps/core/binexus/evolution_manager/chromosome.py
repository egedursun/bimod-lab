#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chromosome.py
#  Last Modified: 2024-10-22 02:45:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 02:45:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import random

import numpy


# Expanded dictionary with gene names and contents


class Chromosome:
    class Tone:
        VERY_SERIOUS = "Very Serious"
        SERIOUS = "Serious"
        NEUTRAL = "Neutral"
        CASUAL = "Casual"
        FRIENDLY = "Friendly"
        HUMOROUS = "Humorous"
        SARCASTIC = "Sarcastic"
        AUTHORITATIVE = "Authoritative"
        EMPATHETIC = "Empathetic"
        CYNICAL = "Cynical"
        EXCITED = "Excited"
        OPTIMISTIC = "Optimistic"
        PESSIMISTIC = "Pessimistic"
        PERSUASIVE = "Persuasive"
        INSPIRING = "Inspiring"
        AGGRESSIVE = "Aggressive"
        PLAYFUL = "Playful"
        THOUGHTFUL = "Thoughtful"
        MELANCHOLIC = "Melancholic"

        @staticmethod
        def as_list():
            return [
                Chromosome.Tone.VERY_SERIOUS, Chromosome.Tone.SERIOUS, Chromosome.Tone.NEUTRAL,
                Chromosome.Tone.CASUAL, Chromosome.Tone.FRIENDLY, Chromosome.Tone.HUMOROUS,
                Chromosome.Tone.SARCASTIC, Chromosome.Tone.AUTHORITATIVE, Chromosome.Tone.EMPATHETIC,
                Chromosome.Tone.CYNICAL, Chromosome.Tone.EXCITED, Chromosome.Tone.OPTIMISTIC,
                Chromosome.Tone.PESSIMISTIC, Chromosome.Tone.PERSUASIVE, Chromosome.Tone.INSPIRING,
                Chromosome.Tone.AGGRESSIVE, Chromosome.Tone.PLAYFUL, Chromosome.Tone.THOUGHTFUL,
                Chromosome.Tone.MELANCHOLIC
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.Tone.as_list()[random.randint(0, len(Chromosome.Tone.as_list()) - 1)]

    class Clarity:
        CRYSTAL_CLEAR = "Crystal Clear"
        VERY_HIGH = "Very High"
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"
        AMBIGUOUS = "Ambiguous"
        SUBTLE = "Subtle"
        IMPLICIT = "Implicit"
        BLUNT = "Blunt"
        OBSCURE = "Obscure"

        @staticmethod
        def as_list():
            return [
                Chromosome.Clarity.CRYSTAL_CLEAR, Chromosome.Clarity.VERY_HIGH, Chromosome.Clarity.HIGH,
                Chromosome.Clarity.MEDIUM, Chromosome.Clarity.LOW, Chromosome.Clarity.AMBIGUOUS,
                Chromosome.Clarity.SUBTLE, Chromosome.Clarity.IMPLICIT, Chromosome.Clarity.BLUNT,
                Chromosome.Clarity.OBSCURE
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.Clarity.as_list()[random.randint(0, len(Chromosome.Clarity.as_list()) - 1)]

    class Format:
        LIST = "List"
        PARAGRAPH = "Paragraph"
        STEP_BY_STEP = "Step-by-step"
        BULLET_POINTS = "Bullet Points"
        TABLE = "Table"
        Q_AND_A = "Q&A"
        DIALOGUE = "Dialogue"
        ESSAY_FORMAT = "Essay Format"
        CODE_BLOCK = "Code Block"
        OUTLINE = "Outline"
        FLOW_CHART = "Flow Chart"
        INFOGRAPHIC_DESCRIPTION = "Infographic Description"
        DIAGRAM = "Diagram"
        MIND_MAP = "Mind Map"
        STORYTELLING = "Storytelling"

        @staticmethod
        def as_list():
            return [
                Chromosome.Format.LIST, Chromosome.Format.PARAGRAPH, Chromosome.Format.STEP_BY_STEP,
                Chromosome.Format.BULLET_POINTS, Chromosome.Format.TABLE, Chromosome.Format.Q_AND_A,
                Chromosome.Format.DIALOGUE, Chromosome.Format.ESSAY_FORMAT, Chromosome.Format.CODE_BLOCK,
                Chromosome.Format.OUTLINE, Chromosome.Format.FLOW_CHART, Chromosome.Format.INFOGRAPHIC_DESCRIPTION,
                Chromosome.Format.DIAGRAM, Chromosome.Format.MIND_MAP, Chromosome.Format.STORYTELLING
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.Format.as_list()[random.randint(0, len(Chromosome.Format.as_list()) - 1)]

    class LengthControl:
        ONE_SENTENCE = "One Sentence"
        SHORT = "Short"
        MEDIUM = "Medium"
        DETAILED = "Detailed"
        EXTENDED = "Extended"
        VERBOSE = "Verbose"
        BREVITY_PREFERRED = "Brevity-Preferred"
        CONCISE = "Concise"
        EXPANSIVE = "Expansive"
        IN_DEPTH = "In-depth"

        @staticmethod
        def as_list():
            return [
                Chromosome.LengthControl.ONE_SENTENCE, Chromosome.LengthControl.SHORT, Chromosome.LengthControl.MEDIUM,
                Chromosome.LengthControl.DETAILED, Chromosome.LengthControl.EXTENDED, Chromosome.LengthControl.VERBOSE,
                Chromosome.LengthControl.BREVITY_PREFERRED, Chromosome.LengthControl.CONCISE,
                Chromosome.LengthControl.EXPANSIVE,
                Chromosome.LengthControl.IN_DEPTH
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.LengthControl.as_list()[random.randint(0, len(Chromosome.LengthControl.as_list()) - 1)]

    class Temperature:
        LOWER_THRESHOLD = 0
        UPPER_THRESHOLD = 2
        INTERVAL_SIZE = 0.025

        @staticmethod
        def as_list():
            return [x for x in numpy.arange(
                Chromosome.Temperature.LOWER_THRESHOLD,
                Chromosome.Temperature.UPPER_THRESHOLD,
                Chromosome.Temperature.INTERVAL_SIZE)]

        @staticmethod
        def get_random_value():
            return Chromosome.Temperature.as_list()[random.randint(0, len(Chromosome.Temperature.as_list()) - 1)]

    class Specificity:
        ULTRA_SPECIFIC = "Ultra-Specific"
        DETAILED = "Detailed"
        MODERATELY_SPECIFIC = "Moderately Specific"
        BROAD = "Broad"
        GENERALIZED = "Generalized"
        FOCUSED = "Focused"
        SPECIALIZED = "Specialized"
        TECHNICAL = "Technical"
        HOLISTIC = "Holistic"
        COMPREHENSIVE = "Comprehensive"

        @staticmethod
        def as_list():
            return [
                Chromosome.Specificity.ULTRA_SPECIFIC, Chromosome.Specificity.DETAILED,
                Chromosome.Specificity.MODERATELY_SPECIFIC, Chromosome.Specificity.BROAD,
                Chromosome.Specificity.GENERALIZED, Chromosome.Specificity.FOCUSED,
                Chromosome.Specificity.SPECIALIZED, Chromosome.Specificity.TECHNICAL,
                Chromosome.Specificity.HOLISTIC, Chromosome.Specificity.COMPREHENSIVE
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.Specificity.as_list()[random.randint(0, len(Chromosome.Specificity.as_list()) - 1)]

    class PromptDepth:
        SHALLOW = "Shallow"
        MODERATE_DEPTH = "Moderate Depth"
        DEEP_ANALYSIS = "Deep Analysis"
        HIGH_LEVEL_OVERVIEW = "High-Level Overview"
        COMPREHENSIVE = "Comprehensive"
        CRITICAL_REVIEW = "Critical Review"
        SURFACE_LEVEL_SUMMARY = "Surface-Level Summary"
        CONCEPTUAL_EXPLORATION = "Conceptual Exploration"
        TECHNICAL_ANALYSIS = "Technical Analysis"

        @staticmethod
        def as_list():
            return [
                Chromosome.PromptDepth.SHALLOW, Chromosome.PromptDepth.MODERATE_DEPTH,
                Chromosome.PromptDepth.DEEP_ANALYSIS, Chromosome.PromptDepth.HIGH_LEVEL_OVERVIEW,
                Chromosome.PromptDepth.COMPREHENSIVE, Chromosome.PromptDepth.CRITICAL_REVIEW,
                Chromosome.PromptDepth.SURFACE_LEVEL_SUMMARY, Chromosome.PromptDepth.CONCEPTUAL_EXPLORATION,
                Chromosome.PromptDepth.TECHNICAL_ANALYSIS
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.PromptDepth.as_list()[random.randint(0, len(Chromosome.PromptDepth.as_list()) - 1)]

    class Perspective:
        FIRST_PERSON = "First-Person"
        THIRD_PERSON = "Third-Person"
        SECOND_PERSON = "Second-Person"
        OBJECTIVE = "Objective"
        SUBJECTIVE = "Subjective"
        THIRD_PERSON_OMNISCIENT = "Third-Person Omniscient"
        LIMITED_FIRST_PERSON = "Limited First-Person"
        NARRATOR_VOICE = "Narrator Voice"
        AUDIENCE_PERSPECTIVE = "Audience Perspective"
        DIALOGUE_BETWEEN_TWO_CHARACTERS = "Dialogue Between Two Characters"

        @staticmethod
        def as_list():
            return [
                Chromosome.Perspective.FIRST_PERSON, Chromosome.Perspective.THIRD_PERSON,
                Chromosome.Perspective.SECOND_PERSON, Chromosome.Perspective.OBJECTIVE,
                Chromosome.Perspective.SUBJECTIVE, Chromosome.Perspective.THIRD_PERSON_OMNISCIENT,
                Chromosome.Perspective.LIMITED_FIRST_PERSON, Chromosome.Perspective.NARRATOR_VOICE,
                Chromosome.Perspective.AUDIENCE_PERSPECTIVE, Chromosome.Perspective.DIALOGUE_BETWEEN_TWO_CHARACTERS
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.Perspective.as_list()[random.randint(0, len(Chromosome.Perspective.as_list()) - 1)]

    class Formality:
        HIGHLY_FORMAL = "Highly Formal"
        FORMAL = "Formal"
        SEMI_FORMAL = "Semi-Formal"
        CASUAL = "Casual"
        COLLOQUIAL = "Colloquial"
        SLANG = "Slang"
        PROFESSIONAL = "Professional"
        CONVERSATIONAL = "Conversational"
        PLAYFUL_FORMALITY = "Playful Formality"
        ACADEMIC = "Academic"
        BUSINESS_TONE = "Business Tone"

        @staticmethod
        def as_list():
            return [
                Chromosome.Formality.HIGHLY_FORMAL, Chromosome.Formality.FORMAL, Chromosome.Formality.SEMI_FORMAL,
                Chromosome.Formality.CASUAL, Chromosome.Formality.COLLOQUIAL, Chromosome.Formality.SLANG,
                Chromosome.Formality.PROFESSIONAL, Chromosome.Formality.CONVERSATIONAL,
                Chromosome.Formality.PLAYFUL_FORMALITY, Chromosome.Formality.ACADEMIC,
                Chromosome.Formality.BUSINESS_TONE
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.Formality.as_list()[random.randint(0, len(Chromosome.Formality.as_list()) - 1)]

    class InstructionStyle:
        DIRECT = "Direct"
        POLITE = "Polite"
        ASSERTIVE = "Assertive"
        GUIDING = "Guiding"
        INQUISITIVE = "Inquisitive"
        SUGGESTIVE = "Suggestive"
        AUTHORITATIVE = "Authoritative"
        COACHING = "Coaching"
        SUPPORTIVE = "Supportive"
        ENCOURAGING = "Encouraging"
        DESCRIPTIVE = "Descriptive"
        INTERACTIVE = "Interactive"
        NEUTRAL = "Neutral"
        OPEN_ENDED = "Open-Ended"
        FACILITATIVE = "Facilitative"

        @staticmethod
        def as_list():
            return [
                Chromosome.InstructionStyle.DIRECT, Chromosome.InstructionStyle.POLITE,
                Chromosome.InstructionStyle.ASSERTIVE, Chromosome.InstructionStyle.GUIDING,
                Chromosome.InstructionStyle.INQUISITIVE, Chromosome.InstructionStyle.SUGGESTIVE,
                Chromosome.InstructionStyle.AUTHORITATIVE, Chromosome.InstructionStyle.COACHING,
                Chromosome.InstructionStyle.SUPPORTIVE, Chromosome.InstructionStyle.ENCOURAGING,
                Chromosome.InstructionStyle.DESCRIPTIVE, Chromosome.InstructionStyle.INTERACTIVE,
                Chromosome.InstructionStyle.NEUTRAL, Chromosome.InstructionStyle.OPEN_ENDED,
                Chromosome.InstructionStyle.FACILITATIVE
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.InstructionStyle.as_list()[
                random.randint(0, len(Chromosome.InstructionStyle.as_list()) - 1)]

    class PolitenessLevel:
        VERY_POLITE = "Very Polite"
        POLITE = "Polite"
        NEUTRAL = "Neutral"
        BLUNT = "Blunt"
        RUDE = "Rude"
        RESPECTFUL = "Respectful"
        DIPLOMATIC = "Diplomatic"
        CORDIAL = "Cordial"
        DIRECT = "Direct"
        SARCASTIC_POLITENESS = "Sarcastic Politeness"

        @staticmethod
        def as_list():
            return [
                Chromosome.PolitenessLevel.VERY_POLITE, Chromosome.PolitenessLevel.POLITE,
                Chromosome.PolitenessLevel.NEUTRAL, Chromosome.PolitenessLevel.BLUNT,
                Chromosome.PolitenessLevel.RUDE, Chromosome.PolitenessLevel.RESPECTFUL,
                Chromosome.PolitenessLevel.DIPLOMATIC, Chromosome.PolitenessLevel.CORDIAL,
                Chromosome.PolitenessLevel.DIRECT, Chromosome.PolitenessLevel.SARCASTIC_POLITENESS
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.PolitenessLevel.as_list()[
                random.randint(0, len(Chromosome.PolitenessLevel.as_list()) - 1)]

    class SentenceComplexity:
        SIMPLE = "Simple"
        COMPOUND = "Compound"
        COMPLEX = "Complex"
        VERY_COMPLEX = "Very Complex"
        FLOWERY = "Flowery"
        MINIMALIST = "Minimalist"
        ELEGANT = "Elegant"
        VERBOSE = "Verbose"
        RUN_ON_SENTENCES = "Run-on Sentences"
        CHOPPY = "Choppy"
        STRUCTURED = "Structured"
        RHYTHMIC = "Rhythmic"

        @staticmethod
        def as_list():
            return [
                Chromosome.SentenceComplexity.SIMPLE, Chromosome.SentenceComplexity.COMPOUND,
                Chromosome.SentenceComplexity.COMPLEX, Chromosome.SentenceComplexity.VERY_COMPLEX,
                Chromosome.SentenceComplexity.FLOWERY, Chromosome.SentenceComplexity.MINIMALIST,
                Chromosome.SentenceComplexity.ELEGANT, Chromosome.SentenceComplexity.VERBOSE,
                Chromosome.SentenceComplexity.RUN_ON_SENTENCES, Chromosome.SentenceComplexity.CHOPPY,
                Chromosome.SentenceComplexity.STRUCTURED, Chromosome.SentenceComplexity.RHYTHMIC
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.SentenceComplexity.as_list()[
                random.randint(0, len(Chromosome.SentenceComplexity.as_list()) - 1)]

    class DetailLevel:
        MINIMAL = "Minimal"
        MODERATE = "Moderate"
        DETAILED = "Detailed"
        EXHAUSTIVE = "Exhaustive"
        METICULOUS = "Meticulous"
        BRIEF_OVERVIEW = "Brief Overview"
        FACTUAL_AND_CONCISE = "Factual and Concise"
        ELABORATE = "Elaborate"
        COMPREHENSIVE_BREAKDOWN = "Comprehensive Breakdown"
        FINE_GRAINED_DETAIL = "Fine-Grained Detail"

        @staticmethod
        def as_list():
            return [
                Chromosome.DetailLevel.MINIMAL, Chromosome.DetailLevel.MODERATE,
                Chromosome.DetailLevel.DETAILED, Chromosome.DetailLevel.EXHAUSTIVE,
                Chromosome.DetailLevel.METICULOUS, Chromosome.DetailLevel.BRIEF_OVERVIEW,
                Chromosome.DetailLevel.FACTUAL_AND_CONCISE, Chromosome.DetailLevel.ELABORATE,
                Chromosome.DetailLevel.COMPREHENSIVE_BREAKDOWN, Chromosome.DetailLevel.FINE_GRAINED_DETAIL
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.DetailLevel.as_list()[random.randint(0, len(Chromosome.DetailLevel.as_list()) - 1)]

    class CriticalThinkingLevel:
        NONE = "None"
        BASIC = "Basic"
        MODERATE = "Moderate"
        HIGH = "High"
        EXTREME = "Extreme"
        ANALYTICAL = "Analytical"
        SKEPTICAL = "Skeptical"
        OPEN_MINDED = "Open-Minded"
        CREATIVE_THINKING = "Creative Thinking"
        RIGOROUS_LOGICAL_REASONING = "Rigorous Logical Reasoning"

        @staticmethod
        def as_list():
            return [
                Chromosome.CriticalThinkingLevel.NONE, Chromosome.CriticalThinkingLevel.BASIC,
                Chromosome.CriticalThinkingLevel.MODERATE, Chromosome.CriticalThinkingLevel.HIGH,
                Chromosome.CriticalThinkingLevel.EXTREME, Chromosome.CriticalThinkingLevel.ANALYTICAL,
                Chromosome.CriticalThinkingLevel.SKEPTICAL, Chromosome.CriticalThinkingLevel.OPEN_MINDED,
                Chromosome.CriticalThinkingLevel.CREATIVE_THINKING,
                Chromosome.CriticalThinkingLevel.RIGOROUS_LOGICAL_REASONING
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.CriticalThinkingLevel.as_list()[
                random.randint(0, len(Chromosome.CriticalThinkingLevel.as_list()) - 1)]

    class LevelOfAssumptions:
        NO_ASSUMPTIONS = "No Assumptions"
        SOME_ASSUMPTIONS = "Some Assumptions"
        MANY_ASSUMPTIONS = "Many Assumptions"
        SPECULATIVE = "Speculative"
        CONSERVATIVE_ASSUMPTIONS = "Conservative Assumptions"
        RISK_TAKING_ASSUMPTIONS = "Risk-Taking Assumptions"
        MINIMALISTIC = "Minimalistic"
        CAUTIOUS = "Cautious"

        @staticmethod
        def as_list():
            return [
                Chromosome.LevelOfAssumptions.NO_ASSUMPTIONS, Chromosome.LevelOfAssumptions.SOME_ASSUMPTIONS,
                Chromosome.LevelOfAssumptions.MANY_ASSUMPTIONS, Chromosome.LevelOfAssumptions.SPECULATIVE,
                Chromosome.LevelOfAssumptions.CONSERVATIVE_ASSUMPTIONS,
                Chromosome.LevelOfAssumptions.RISK_TAKING_ASSUMPTIONS,
                Chromosome.LevelOfAssumptions.MINIMALISTIC, Chromosome.LevelOfAssumptions.CAUTIOUS
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.LevelOfAssumptions.as_list()[
                random.randint(0, len(Chromosome.LevelOfAssumptions.as_list()) - 1)]

    class CulturalSensitivity:
        HIGHLY_SENSITIVE = "Highly Sensitive"
        MODERATELY_SENSITIVE = "Moderately Sensitive"
        NEUTRAL = "Neutral"
        INSENSITIVE = "Insensitive"
        HYPER_AWARE = "Hyper-Aware"
        GLOBALLY_INCLUSIVE = "Globally Inclusive"
        CONTEXTUALLY_SENSITIVE = "Contextually Sensitive"
        REGIONALLY_FOCUSED = "Regionally Focused"
        MULTICULTURAL_AWARENESS = "Multicultural Awareness"

        @staticmethod
        def as_list():
            return [
                Chromosome.CulturalSensitivity.HIGHLY_SENSITIVE, Chromosome.CulturalSensitivity.MODERATELY_SENSITIVE,
                Chromosome.CulturalSensitivity.NEUTRAL, Chromosome.CulturalSensitivity.INSENSITIVE,
                Chromosome.CulturalSensitivity.HYPER_AWARE, Chromosome.CulturalSensitivity.GLOBALLY_INCLUSIVE,
                Chromosome.CulturalSensitivity.CONTEXTUALLY_SENSITIVE,
                Chromosome.CulturalSensitivity.REGIONALLY_FOCUSED,
                Chromosome.CulturalSensitivity.MULTICULTURAL_AWARENESS
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.CulturalSensitivity.as_list()[
                random.randint(0, len(Chromosome.CulturalSensitivity.as_list()) - 1)]

    class TargetAudience:
        EXPERTS = "Experts"
        NOVICES = "Novices"
        CHILDREN = "Children"
        ADULTS = "Adults"
        ACADEMICS = "Academics"
        EXECUTIVES = "Executives"
        GENERAL_PUBLIC = "General Public"
        TECHNICAL = "Technical"
        LAYMAN = "Layman"
        ENTREPRENEURS = "Entrepreneurs"
        HEALTHCARE_PROFESSIONALS = "Healthcare Professionals"
        RESEARCHERS = "Researchers"
        DEVELOPERS = "Developers"
        DESIGNERS = "Designers"
        MARKETERS = "Marketers"
        LEGAL_PROFESSIONALS = "Legal Professionals"

        @staticmethod
        def as_list():
            return [
                Chromosome.TargetAudience.EXPERTS, Chromosome.TargetAudience.NOVICES,
                Chromosome.TargetAudience.CHILDREN, Chromosome.TargetAudience.ADULTS,
                Chromosome.TargetAudience.ACADEMICS, Chromosome.TargetAudience.EXECUTIVES,
                Chromosome.TargetAudience.GENERAL_PUBLIC, Chromosome.TargetAudience.TECHNICAL,
                Chromosome.TargetAudience.LAYMAN, Chromosome.TargetAudience.ENTREPRENEURS,
                Chromosome.TargetAudience.HEALTHCARE_PROFESSIONALS, Chromosome.TargetAudience.RESEARCHERS,
                Chromosome.TargetAudience.DEVELOPERS, Chromosome.TargetAudience.DESIGNERS,
                Chromosome.TargetAudience.MARKETERS, Chromosome.TargetAudience.LEGAL_PROFESSIONALS
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.TargetAudience.as_list()[random.randint(0, len(Chromosome.TargetAudience.as_list()) - 1)]

    class JargonLevel:
        NO_JARGON = "No Jargon"
        BASIC_JARGON = "Basic Jargon"
        MODERATE_TECHNICAL_JARGON = "Moderate Technical Jargon"
        HIGHLY_TECHNICAL = "Highly Technical"
        INDUSTRY_SPECIFIC = "Industry-Specific"
        ACCESSIBLE = "Accessible"
        SPECIALIZED_TERMINOLOGY = "Specialized Terminology"

        @staticmethod
        def as_list():
            return [
                Chromosome.JargonLevel.NO_JARGON, Chromosome.JargonLevel.BASIC_JARGON,
                Chromosome.JargonLevel.MODERATE_TECHNICAL_JARGON, Chromosome.JargonLevel.HIGHLY_TECHNICAL,
                Chromosome.JargonLevel.INDUSTRY_SPECIFIC, Chromosome.JargonLevel.ACCESSIBLE,
                Chromosome.JargonLevel.SPECIALIZED_TERMINOLOGY
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.JargonLevel.as_list()[random.randint(0, len(Chromosome.JargonLevel.as_list()) - 1)]

    class TimeSensitivity:
        IMMEDIATE = "Immediate"
        SHORT_TERM = "Short-Term"
        LONG_TERM = "Long-Term"
        TIMELESS = "Timeless"
        HISTORICAL_CONTEXT = "Historical Context"
        FUTURE_ORIENTED = "Future-Oriented"
        PRESENT_FOCUSED = "Present-Focused"
        RETROSPECTIVE = "Retrospective"
        PREDICTIVE = "Predictive"
        URGENT = "Urgent"

        @staticmethod
        def as_list():
            return [
                Chromosome.TimeSensitivity.IMMEDIATE, Chromosome.TimeSensitivity.SHORT_TERM,
                Chromosome.TimeSensitivity.LONG_TERM, Chromosome.TimeSensitivity.TIMELESS,
                Chromosome.TimeSensitivity.HISTORICAL_CONTEXT, Chromosome.TimeSensitivity.FUTURE_ORIENTED,
                Chromosome.TimeSensitivity.PRESENT_FOCUSED, Chromosome.TimeSensitivity.RETROSPECTIVE,
                Chromosome.TimeSensitivity.PREDICTIVE, Chromosome.TimeSensitivity.URGENT
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.TimeSensitivity.as_list()[
                random.randint(0, len(Chromosome.TimeSensitivity.as_list()) - 1)]

    class BiasOrObjectivity:
        HIGHLY_OBJECTIVE = "Highly Objective"
        MODERATELY_OBJECTIVE = "Moderately Objective"
        BALANCED = "Balanced"
        MILDLY_BIASED = "Mildly Biased"
        HIGHLY_BIASED = "Highly Biased"
        PERSUASIVE_BIAS = "Persuasive Bias"
        CRITICAL_OBJECTIVITY = "Critical Objectivity"
        OPINIONATED = "Opinionated"
        FAIRLY_BALANCED = "Fairly Balanced"

        @staticmethod
        def as_list():
            return [
                Chromosome.BiasOrObjectivity.HIGHLY_OBJECTIVE, Chromosome.BiasOrObjectivity.MODERATELY_OBJECTIVE,
                Chromosome.BiasOrObjectivity.BALANCED, Chromosome.BiasOrObjectivity.MILDLY_BIASED,
                Chromosome.BiasOrObjectivity.HIGHLY_BIASED, Chromosome.BiasOrObjectivity.PERSUASIVE_BIAS,
                Chromosome.BiasOrObjectivity.CRITICAL_OBJECTIVITY, Chromosome.BiasOrObjectivity.OPINIONATED,
                Chromosome.BiasOrObjectivity.FAIRLY_BALANCED
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.BiasOrObjectivity.as_list()[
                random.randint(0, len(Chromosome.BiasOrObjectivity.as_list()) - 1)]

    class FactualAccuracy:
        STRICTLY_FACTUAL = "Strictly Factual"
        MODERATELY_ACCURATE = "Moderately Accurate"
        CREATIVE_FLEXIBILITY = "Creative Flexibility"
        SPECULATIVE = "Speculative"
        VERIFIED_FACTS = "Verified Facts"
        LOOSE_FACTS_WITH_CREATIVITY = "Loose Facts with Creativity"
        EVIDENCE_BASED = "Evidence-Based"

        @staticmethod
        def as_list():
            return [
                Chromosome.FactualAccuracy.STRICTLY_FACTUAL, Chromosome.FactualAccuracy.MODERATELY_ACCURATE,
                Chromosome.FactualAccuracy.CREATIVE_FLEXIBILITY, Chromosome.FactualAccuracy.SPECULATIVE,
                Chromosome.FactualAccuracy.VERIFIED_FACTS, Chromosome.FactualAccuracy.LOOSE_FACTS_WITH_CREATIVITY,
                Chromosome.FactualAccuracy.EVIDENCE_BASED
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.FactualAccuracy.as_list()[
                random.randint(0, len(Chromosome.FactualAccuracy.as_list()) - 1)]

    class EmotionalIntensity:
        HIGH_EMOTION = "High Emotion"
        MODERATE_EMOTION = "Moderate Emotion"
        NEUTRAL_EMOTION = "Neutral Emotion"
        DISPASSIONATE = "Dispassionate"
        EMPATHIC = "Empathic"
        COLD_AND_DETACHED = "Cold and Detached"
        SENTIMENTAL = "Sentimental"
        EMOTIONALLY_NEUTRAL = "Emotionally Neutral"
        HIGH_EMPATHY = "High Empathy"

        @staticmethod
        def as_list():
            return [
                Chromosome.EmotionalIntensity.HIGH_EMOTION, Chromosome.EmotionalIntensity.MODERATE_EMOTION,
                Chromosome.EmotionalIntensity.NEUTRAL_EMOTION, Chromosome.EmotionalIntensity.DISPASSIONATE,
                Chromosome.EmotionalIntensity.EMPATHIC, Chromosome.EmotionalIntensity.COLD_AND_DETACHED,
                Chromosome.EmotionalIntensity.SENTIMENTAL, Chromosome.EmotionalIntensity.EMOTIONALLY_NEUTRAL,
                Chromosome.EmotionalIntensity.HIGH_EMPATHY
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.EmotionalIntensity.as_list()[
                random.randint(0, len(Chromosome.EmotionalIntensity.as_list()) - 1)]

    class RhetoricalStyle:
        PERSUASIVE = "Persuasive"
        DESCRIPTIVE = "Descriptive"
        NARRATIVE = "Narrative"
        EXPOSITORY = "Expository"
        ARGUMENTATIVE = "Argumentative"
        DIDACTIC = "Didactic"
        POETIC = "Poetic"
        REFLECTIVE = "Reflective"
        RHETORICAL_QUESTIONING = "Rhetorical Questioning"
        PHILOSOPHICAL = "Philosophical"

        @staticmethod
        def as_list():
            return [
                Chromosome.RhetoricalStyle.PERSUASIVE, Chromosome.RhetoricalStyle.DESCRIPTIVE,
                Chromosome.RhetoricalStyle.NARRATIVE, Chromosome.RhetoricalStyle.EXPOSITORY,
                Chromosome.RhetoricalStyle.ARGUMENTATIVE, Chromosome.RhetoricalStyle.DIDACTIC,
                Chromosome.RhetoricalStyle.POETIC, Chromosome.RhetoricalStyle.REFLECTIVE,
                Chromosome.RhetoricalStyle.RHETORICAL_QUESTIONING, Chromosome.RhetoricalStyle.PHILOSOPHICAL
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.RhetoricalStyle.as_list()[
                random.randint(0, len(Chromosome.RhetoricalStyle.as_list()) - 1)]

    class TaskIterationAndFeedback:
        ONE_OFF_TASK = "One-off Task"
        REPETITIVE_TASK = "Repetitive Task"
        ITERATIVE_TASK = "Iterative Task"
        TASK_WITH_FEEDBACK_LOOPS = "Task with Feedback Loops"
        COLLABORATIVE_TASK = "Collaborative Task"
        SEQUENTIAL_TASK = "Sequential Task"
        ADAPTIVE_FEEDBACK = "Adaptive Feedback"

        @staticmethod
        def as_list():
            return [
                Chromosome.TaskIterationAndFeedback.ONE_OFF_TASK, Chromosome.TaskIterationAndFeedback.REPETITIVE_TASK,
                Chromosome.TaskIterationAndFeedback.ITERATIVE_TASK,
                Chromosome.TaskIterationAndFeedback.TASK_WITH_FEEDBACK_LOOPS,
                Chromosome.TaskIterationAndFeedback.COLLABORATIVE_TASK,
                Chromosome.TaskIterationAndFeedback.SEQUENTIAL_TASK,
                Chromosome.TaskIterationAndFeedback.ADAPTIVE_FEEDBACK
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.TaskIterationAndFeedback.as_list()[
                random.randint(0, len(Chromosome.TaskIterationAndFeedback.as_list()) - 1)]

    class BiasForSimplicityVsComplexity:
        FAVOR_SIMPLICITY = "Favor Simplicity"
        BALANCED = "Balanced"
        FAVOR_COMPLEXITY = "Favor Complexity"
        EXTREME_SIMPLICITY = "Extreme Simplicity"
        MAXIMIZED_COMPLEXITY = "Maximized Complexity"
        ELEGANT_SIMPLICITY = "Elegant Simplicity"

        @staticmethod
        def as_list():
            return [
                Chromosome.BiasForSimplicityVsComplexity.FAVOR_SIMPLICITY,
                Chromosome.BiasForSimplicityVsComplexity.BALANCED,
                Chromosome.BiasForSimplicityVsComplexity.FAVOR_COMPLEXITY,
                Chromosome.BiasForSimplicityVsComplexity.EXTREME_SIMPLICITY,
                Chromosome.BiasForSimplicityVsComplexity.MAXIMIZED_COMPLEXITY,
                Chromosome.BiasForSimplicityVsComplexity.ELEGANT_SIMPLICITY
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.BiasForSimplicityVsComplexity.as_list()[
                random.randint(0, len(Chromosome.BiasForSimplicityVsComplexity.as_list()) - 1)]

    class CreativeFreedom:
        NO_FREEDOM = "No Freedom"
        MODERATE = "Moderate"
        HIGH = "High"
        FULL_CREATIVITY = "Full Creativity"
        CONSTRAINED_CREATIVITY = "Constrained Creativity"
        GUIDED_INNOVATION = "Guided Innovation"

        @staticmethod
        def as_list():
            return [
                Chromosome.CreativeFreedom.NO_FREEDOM, Chromosome.CreativeFreedom.MODERATE,
                Chromosome.CreativeFreedom.HIGH, Chromosome.CreativeFreedom.FULL_CREATIVITY,
                Chromosome.CreativeFreedom.CONSTRAINED_CREATIVITY, Chromosome.CreativeFreedom.GUIDED_INNOVATION
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.CreativeFreedom.as_list()[
                random.randint(0, len(Chromosome.CreativeFreedom.as_list()) - 1)]

    class InstructionRedundancy:
        NO_REDUNDANCY = "No Redundancy"
        SOME_REDUNDANCY = "Some Redundancy"
        HIGH_REDUNDANCY = "High Redundancy"
        REPETITIVE_INSTRUCTION = "Repetitive Instruction"
        REINFORCED_INSTRUCTION = "Reinforced Instruction"

        @staticmethod
        def as_list():
            return [
                Chromosome.InstructionRedundancy.NO_REDUNDANCY, Chromosome.InstructionRedundancy.SOME_REDUNDANCY,
                Chromosome.InstructionRedundancy.HIGH_REDUNDANCY,
                Chromosome.InstructionRedundancy.REPETITIVE_INSTRUCTION,
                Chromosome.InstructionRedundancy.REINFORCED_INSTRUCTION
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.InstructionRedundancy.as_list()[
                random.randint(0, len(Chromosome.InstructionRedundancy.as_list()) - 1)]

    class EvidenceAndCitation:
        NO_EVIDENCE_NEEDED = "No Evidence Needed"
        SOME_EVIDENCE = "Some Evidence"
        HIGHLY_CITED = "Highly Cited"
        ONLY_AUTHORITATIVE_SOURCES = "Only Authoritative Sources"
        PERSONAL_ANECDOTES = "Personal Anecdotes"
        PEER_REVIEWED_SOURCES = "Peer-Reviewed Sources"
        HISTORICAL_EVIDENCE = "Historical Evidence"
        DATA_DRIVEN = "Data-Driven"

        @staticmethod
        def as_list():
            return [
                Chromosome.EvidenceAndCitation.NO_EVIDENCE_NEEDED, Chromosome.EvidenceAndCitation.SOME_EVIDENCE,
                Chromosome.EvidenceAndCitation.HIGHLY_CITED, Chromosome.EvidenceAndCitation.ONLY_AUTHORITATIVE_SOURCES,
                Chromosome.EvidenceAndCitation.PERSONAL_ANECDOTES,
                Chromosome.EvidenceAndCitation.PEER_REVIEWED_SOURCES,
                Chromosome.EvidenceAndCitation.HISTORICAL_EVIDENCE, Chromosome.EvidenceAndCitation.DATA_DRIVEN
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.EvidenceAndCitation.as_list()[
                random.randint(0, len(Chromosome.EvidenceAndCitation.as_list()) - 1)]

    class HumorAndPlayfulness:
        NO_HUMOR = "No Humor"
        SUBTLE = "Subtle"
        MODERATE = "Moderate"
        HUMOROUS = "Humorous"
        PLAYFUL = "Playful"
        WITTY = "Witty"
        DRY_HUMOR = "Dry Humor"
        SARCASTIC_HUMOR = "Sarcastic Humor"
        CLEVER_PLAYFULNESS = "Clever Playfulness"

        @staticmethod
        def as_list():
            return [
                Chromosome.HumorAndPlayfulness.NO_HUMOR, Chromosome.HumorAndPlayfulness.SUBTLE,
                Chromosome.HumorAndPlayfulness.MODERATE, Chromosome.HumorAndPlayfulness.HUMOROUS,
                Chromosome.HumorAndPlayfulness.PLAYFUL, Chromosome.HumorAndPlayfulness.WITTY,
                Chromosome.HumorAndPlayfulness.DRY_HUMOR, Chromosome.HumorAndPlayfulness.SARCASTIC_HUMOR,
                Chromosome.HumorAndPlayfulness.CLEVER_PLAYFULNESS
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.HumorAndPlayfulness.as_list()[
                random.randint(0, len(Chromosome.HumorAndPlayfulness.as_list()) - 1)]

    class AudienceEngagement:
        PASSIVE = "Passive"
        NEUTRAL = "Neutral"
        ACTIVE_ENGAGEMENT = "Active Engagement"
        HIGHLY_INTERACTIVE = "Highly Interactive"
        PARTICIPATORY = "Participatory"
        INQUISITIVE = "Inquisitive"
        RESPONSIVE = "Responsive"
        CALL_TO_ACTION = "Call to Action"

        @staticmethod
        def as_list():
            return [
                Chromosome.AudienceEngagement.PASSIVE, Chromosome.AudienceEngagement.NEUTRAL,
                Chromosome.AudienceEngagement.ACTIVE_ENGAGEMENT, Chromosome.AudienceEngagement.HIGHLY_INTERACTIVE,
                Chromosome.AudienceEngagement.PARTICIPATORY, Chromosome.AudienceEngagement.INQUISITIVE,
                Chromosome.AudienceEngagement.RESPONSIVE, Chromosome.AudienceEngagement.CALL_TO_ACTION
            ]

        @staticmethod
        def get_random_value():
            return Chromosome.AudienceEngagement.as_list()[
                random.randint(0, len(Chromosome.AudienceEngagement.as_list()) - 1)]

    class GeneNames:
        TONE = "Tone"
        CLARITY = "Clarity"
        FORMAT = "Format"
        LENGTH_CONTROL = "LengthControl"
        TEMPERATURE = "Temperature"
        SPECIFICITY = "Specificity"
        PROMPT_DEPTH = "PromptDepth"
        PERSPECTIVE = "Perspective"
        FORMALITY = "Formality"
        INSTRUCTION_STYLE = "InstructionStyle"
        POLITENESS_LEVEL = "PolitenessLevel"
        SENTENCE_COMPLEXITY = "SentenceComplexity"
        DETAIL_LEVEL = "DetailLevel"
        CRITICAL_THINKING_LEVEL = "CriticalThinkingLevel"
        LEVEL_OF_ASSUMPTIONS = "LevelOfAssumptions"
        CULTURAL_SENSITIVITY = "CulturalSensitivity"
        TARGET_AUDIENCE = "TargetAudience"
        JARGON_LEVEL = "JargonLevel"
        TIME_SENSITIVITY = "TimeSensitivity"
        BIAS_OR_OBJECTIVITY = "BiasOrObjectivity"
        FACTUAL_ACCURACY = "FactualAccuracy"
        EMOTIONAL_INTENSITY = "EmotionalIntensity"
        RHETORICAL_STYLE = "RhetoricalStyle"
        TASK_ITERATION_AND_FEEDBACK = "TaskIterationAndFeedback"
        BIAS_FOR_SIMPLICITY_VS_COMPLEXITY = "BiasForSimplicityVsComplexity"
        CREATIVE_FREEDOM = "CreativeFreedom"
        INSTRUCTION_REDUNDANCY = "InstructionRedundancy"
        EVIDENCE_AND_CITATION = "EvidenceAndCitation"
        HUMOR_AND_PLAYFULNESS = "HumorAndPlayfulness"
        AUDIENCE_ENGAGEMENT = "AudienceEngagement"

        @staticmethod
        def as_list():
            return [
                Chromosome.GeneNames.TONE, Chromosome.GeneNames.CLARITY, Chromosome.GeneNames.FORMAT,
                Chromosome.GeneNames.LENGTH_CONTROL, Chromosome.GeneNames.TEMPERATURE,
                Chromosome.GeneNames.SPECIFICITY,
                Chromosome.GeneNames.PROMPT_DEPTH, Chromosome.GeneNames.PERSPECTIVE, Chromosome.GeneNames.FORMALITY,
                Chromosome.GeneNames.INSTRUCTION_STYLE, Chromosome.GeneNames.POLITENESS_LEVEL,
                Chromosome.GeneNames.SENTENCE_COMPLEXITY,
                Chromosome.GeneNames.DETAIL_LEVEL, Chromosome.GeneNames.CRITICAL_THINKING_LEVEL,
                Chromosome.GeneNames.LEVEL_OF_ASSUMPTIONS,
                Chromosome.GeneNames.CULTURAL_SENSITIVITY, Chromosome.GeneNames.TARGET_AUDIENCE,
                Chromosome.GeneNames.JARGON_LEVEL,
                Chromosome.GeneNames.TIME_SENSITIVITY, Chromosome.GeneNames.BIAS_OR_OBJECTIVITY,
                Chromosome.GeneNames.FACTUAL_ACCURACY,
                Chromosome.GeneNames.EMOTIONAL_INTENSITY, Chromosome.GeneNames.RHETORICAL_STYLE,
                Chromosome.GeneNames.TASK_ITERATION_AND_FEEDBACK,
                Chromosome.GeneNames.BIAS_FOR_SIMPLICITY_VS_COMPLEXITY, Chromosome.GeneNames.CREATIVE_FREEDOM,
                Chromosome.GeneNames.INSTRUCTION_REDUNDANCY,
                Chromosome.GeneNames.EVIDENCE_AND_CITATION, Chromosome.GeneNames.HUMOR_AND_PLAYFULNESS,
                Chromosome.GeneNames.AUDIENCE_ENGAGEMENT
            ]

        @staticmethod
        def get_random_gene():
            return Chromosome.GeneNames.as_list()[random.randint(0, len(Chromosome.GeneNames.as_list()) - 1)]

    ############

    @staticmethod
    def get_random_chromosome():
        return {
            Chromosome.GeneNames.TONE: Chromosome.Tone.get_random_value(),
            Chromosome.GeneNames.CLARITY: Chromosome.Clarity.get_random_value(),
            Chromosome.GeneNames.FORMAT: Chromosome.Format.get_random_value(),
            Chromosome.GeneNames.LENGTH_CONTROL: Chromosome.LengthControl.get_random_value(),
            Chromosome.GeneNames.TEMPERATURE: Chromosome.Temperature.get_random_value(),
            Chromosome.GeneNames.SPECIFICITY: Chromosome.Specificity.get_random_value(),
            Chromosome.GeneNames.PROMPT_DEPTH: Chromosome.PromptDepth.get_random_value(),
            Chromosome.GeneNames.PERSPECTIVE: Chromosome.Perspective.get_random_value(),
            Chromosome.GeneNames.FORMALITY: Chromosome.Formality.get_random_value(),
            Chromosome.GeneNames.INSTRUCTION_STYLE: Chromosome.InstructionStyle.get_random_value(),
            Chromosome.GeneNames.POLITENESS_LEVEL: Chromosome.PolitenessLevel.get_random_value(),
            Chromosome.GeneNames.SENTENCE_COMPLEXITY: Chromosome.SentenceComplexity.get_random_value(),
            Chromosome.GeneNames.DETAIL_LEVEL: Chromosome.DetailLevel.get_random_value(),
            Chromosome.GeneNames.CRITICAL_THINKING_LEVEL: Chromosome.CriticalThinkingLevel.get_random_value(),
            Chromosome.GeneNames.LEVEL_OF_ASSUMPTIONS: Chromosome.LevelOfAssumptions.get_random_value(),
            Chromosome.GeneNames.CULTURAL_SENSITIVITY: Chromosome.CulturalSensitivity.get_random_value(),
            Chromosome.GeneNames.TARGET_AUDIENCE: Chromosome.TargetAudience.get_random_value(),
            Chromosome.GeneNames.JARGON_LEVEL: Chromosome.JargonLevel.get_random_value(),
            Chromosome.GeneNames.TIME_SENSITIVITY: Chromosome.TimeSensitivity.get_random_value(),
            Chromosome.GeneNames.BIAS_OR_OBJECTIVITY: Chromosome.BiasOrObjectivity.get_random_value(),
            Chromosome.GeneNames.FACTUAL_ACCURACY: Chromosome.FactualAccuracy.get_random_value(),
            Chromosome.GeneNames.EMOTIONAL_INTENSITY: Chromosome.EmotionalIntensity.get_random_value(),
            Chromosome.GeneNames.RHETORICAL_STYLE: Chromosome.RhetoricalStyle.get_random_value(),
            Chromosome.GeneNames.TASK_ITERATION_AND_FEEDBACK: Chromosome.TaskIterationAndFeedback.get_random_value(),
            Chromosome.GeneNames.BIAS_FOR_SIMPLICITY_VS_COMPLEXITY: Chromosome.BiasForSimplicityVsComplexity.get_random_value(),
            Chromosome.GeneNames.CREATIVE_FREEDOM: Chromosome.CreativeFreedom.get_random_value(),
            Chromosome.GeneNames.INSTRUCTION_REDUNDANCY: Chromosome.InstructionRedundancy.get_random_value(),
            Chromosome.GeneNames.EVIDENCE_AND_CITATION: Chromosome.EvidenceAndCitation.get_random_value(),
            Chromosome.GeneNames.HUMOR_AND_PLAYFULNESS: Chromosome.HumorAndPlayfulness.get_random_value(),
            Chromosome.GeneNames.AUDIENCE_ENGAGEMENT: Chromosome.AudienceEngagement.get_random_value(),
        }

    @staticmethod
    def give_random_value_of_gene(gene_name: str):
        if gene_name == Chromosome.GeneNames.TONE:
            return Chromosome.Tone.get_random_value()
        elif gene_name == Chromosome.GeneNames.CLARITY:
            return Chromosome.Clarity.get_random_value()
        elif gene_name == Chromosome.GeneNames.FORMAT:
            return Chromosome.Format.get_random_value()
        elif gene_name == Chromosome.GeneNames.LENGTH_CONTROL:
            return Chromosome.LengthControl.get_random_value()
        elif gene_name == Chromosome.GeneNames.TEMPERATURE:
            return Chromosome.Temperature.get_random_value()
        elif gene_name == Chromosome.GeneNames.SPECIFICITY:
            return Chromosome.Specificity.get_random_value()
        elif gene_name == Chromosome.GeneNames.PROMPT_DEPTH:
            return Chromosome.PromptDepth.get_random_value()
        elif gene_name == Chromosome.GeneNames.PERSPECTIVE:
            return Chromosome.Perspective.get_random_value()
        elif gene_name == Chromosome.GeneNames.FORMALITY:
            return Chromosome.Formality.get_random_value()
        elif gene_name == Chromosome.GeneNames.INSTRUCTION_STYLE:
            return Chromosome.InstructionStyle.get_random_value()
        elif gene_name == Chromosome.GeneNames.POLITENESS_LEVEL:
            return Chromosome.PolitenessLevel.get_random_value()
        elif gene_name == Chromosome.GeneNames.SENTENCE_COMPLEXITY:
            return Chromosome.SentenceComplexity.get_random_value()
        elif gene_name == Chromosome.GeneNames.DETAIL_LEVEL:
            return Chromosome.DetailLevel.get_random_value()
        elif gene_name == Chromosome.GeneNames.CRITICAL_THINKING_LEVEL:
            return Chromosome.CriticalThinkingLevel.get_random_value()
        elif gene_name == Chromosome.GeneNames.LEVEL_OF_ASSUMPTIONS:
            return Chromosome.LevelOfAssumptions.get_random_value()
        elif gene_name == Chromosome.GeneNames.CULTURAL_SENSITIVITY:
            return Chromosome.CulturalSensitivity.get_random_value()
        elif gene_name == Chromosome.GeneNames.TARGET_AUDIENCE:
            return Chromosome.TargetAudience.get_random_value()
        elif gene_name == Chromosome.GeneNames.JARGON_LEVEL:
            return Chromosome.JargonLevel.get_random_value()
        elif gene_name == Chromosome.GeneNames.TIME_SENSITIVITY:
            return Chromosome.TimeSensitivity.get_random_value()
        elif gene_name == Chromosome.GeneNames.BIAS_OR_OBJECTIVITY:
            return Chromosome.BiasOrObjectivity.get_random_value()
        elif gene_name == Chromosome.GeneNames.FACTUAL_ACCURACY:
            return Chromosome.FactualAccuracy.get_random_value()
        elif gene_name == Chromosome.GeneNames.EMOTIONAL_INTENSITY:
            return Chromosome.EmotionalIntensity.get_random_value()
        elif gene_name == Chromosome.GeneNames.RHETORICAL_STYLE:
            return Chromosome.RhetoricalStyle.get_random_value()
        elif gene_name == Chromosome.GeneNames.TASK_ITERATION_AND_FEEDBACK:
            return Chromosome.TaskIterationAndFeedback.get_random_value()
        elif gene_name == Chromosome.GeneNames.BIAS_FOR_SIMPLICITY_VS_COMPLEXITY:
            return Chromosome.BiasForSimplicityVsComplexity.get_random_value()
        elif gene_name == Chromosome.GeneNames.CREATIVE_FREEDOM:
            return Chromosome.CreativeFreedom.get_random_value()
        elif gene_name == Chromosome.GeneNames.INSTRUCTION_REDUNDANCY:
            return Chromosome.InstructionRedundancy.get_random_value()
        elif gene_name == Chromosome.GeneNames.EVIDENCE_AND_CITATION:
            return Chromosome.EvidenceAndCitation.get_random_value()
        elif gene_name == Chromosome.GeneNames.HUMOR_AND_PLAYFULNESS:
            return Chromosome.HumorAndPlayfulness.get_random_value()
        elif gene_name == Chromosome.GeneNames.AUDIENCE_ENGAGEMENT:
            return Chromosome.AudienceEngagement.get_random_value()
        else:
            return None

    @staticmethod
    def get_index_of_gene(gene_name: str):
        return Chromosome.GeneNames.as_list().index(gene_name)

    @staticmethod
    def get_class_name_of_gene(gene_name: str):
        return Chromosome.GeneNames.as_list()[Chromosome.get_index_of_gene(gene_name)]

    @staticmethod
    def get_index_of_gene_value(gene_name: str, gene_value: str):
        class_name = Chromosome.get_class_name_of_gene(gene_name)
        gene_value_index = Chromosome.__dict__[class_name].as_list().index(gene_value)
        return gene_value_index
