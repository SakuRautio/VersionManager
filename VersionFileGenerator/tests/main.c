/**
 * The test runner for verifying that the scripts
 * work and that they are able to be used in programs.
 *
 * Author: Saku Rautio
 * Date: 2020-02-02
 * License: MIT
 */

#include <stdio.h>

#include "version.h"

int main(void)
{
   printf("Start of tests!\r\n");

   printf(
      "Version:{\r\n"
      "\tMajor: %d,\r\n"
      "\tMinor: %d,\r\n"
      "\tBug: %d,\r\n"
      "\tStage: %d,\r\n"
      "\tStageRev: %d,\r\n"
      "}\r\n",
      version.major, version.minor, version.bug, version.stage, version.stageRev
   );
   
   printf("End of tests!\r\n");
   return 0;
}
