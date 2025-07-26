# Responsible AI Guidelines for RentBot

We designed **RentBot** with responsible AI principles:

## Transparency
- Clear indication that predictions are based on historical sample data.
- Simple, explainable linear model to avoid "black box" behavior.

## Bias Mitigation
- Dataset includes diverse property types from multiple districts to reduce bias.
- No demographic or sensitive data used.

## Privacy
- No personal user data is stored or logged.
- Users only input property attributes (district, type, bedrooms, etc.).

## Reliability
- Model predictions are approximate and include disclaimers in the README.
- Tested with edge cases to avoid invalid outputs.

## Future Improvements
- Regular dataset updates to improve fairness.
- Integration with live housing data while maintaining ethical standards.
