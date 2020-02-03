/**
 * Project's Git version tag definition as a struct.
 *
 * Author: Saku Rautio
 * Date: 2020-02-02
 * License: MIT
 *
 * Has the following format:
 *     [major].[minor].[bug]-[stage].[stage revision]
 * E.g.:
 *     1.2.1-rc.3
 *         * Major: 1
 *         * Minor: 2
 *         * Bug: 1
 *         * Stage: Release Canditate
 *         * Stage Revision: 3
 *
 * Takes 5 bytes at minimum to be stored in memory.
 * 
 * NOTE: Depending on the compiler's implementation on
 * how it handles the size of an enum it can be
 * either UINT8_MAX or something bigger.
 */

#include <stdint.h>

typedef enum stage {
    STAGE_DEVELOPMENT = 0x00,
    STAGE_RELEASE = 0x01,
    STAGE_RELEASE_CANDIDATE = 0x02,
    STAGE_ALPHA = 0x03,
    STAGE_BETA = 0x04,
    STAGE_MAX = UINT8_MAX
} version_stage_t;

typedef struct version {
    uint8_t major;         // Major:          0 .. 255
    uint8_t minor;         // Minor:          0 .. 255
    uint8_t bug;           // Bug:            0 .. 255
    version_stage_t stage; // Stage:          0 .. 255
    uint8_t stageRev;      // Stage Revision: 0 .. 255
} version_t;

extern version_t version;
