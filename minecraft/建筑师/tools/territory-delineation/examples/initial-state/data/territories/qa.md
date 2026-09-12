# 几何 QA

4-neighbor; adjacency counts shared unit land edges; water crossings excluded. Enclave candidate: no water/study edge and exactly one surrounding other class. Fragment: area<threshold; disconnected areas may be natural islands. UNASSIGNED/DISPUTED are explicit classes, not errors repaired automatically.

状态：DRAFT

未分配：2150896；争议：0；accepted geometry 改动：0。

ALLIANCE_COMMONS: 1 连通片，0 小于 64 格的碎片，0 飞地候选。

WEST_DOMAIN: 0 连通片，0 小于 64 格的碎片，0 飞地候选。

MIDDLE_DOMAIN: 1 连通片，0 小于 64 格的碎片，0 飞地候选。

EAST_DOMAIN: 0 连通片，0 小于 64 格的碎片，0 飞地候选。

UNASSIGNED: 2102 连通片，2097 小于 64 格的碎片，0 飞地候选。

DISPUTED: 0 连通片，0 小于 64 格的碎片，0 飞地候选。

完整几何诊断：
```json
{
  "revision": 6,
  "landColumns": 2256681,
  "areas": [
    92124,
    0,
    13661,
    0,
    2150896,
    0
  ],
  "unassigned": 2150896,
  "disputed": 0,
  "acceptedChanged": 0,
  "adjacency": [
    [
      0,
      0,
      48,
      0,
      0,
      0
    ],
    [
      0,
      0,
      0,
      0,
      0,
      0
    ],
    [
      48,
      0,
      0,
      0,
      190,
      0
    ],
    [
      0,
      0,
      0,
      0,
      0,
      0
    ],
    [
      0,
      0,
      190,
      0,
      0,
      0
    ],
    [
      0,
      0,
      0,
      0,
      0,
      0
    ]
  ],
  "shoreEdges": [
    1736,
    0,
    562,
    0,
    38858,
    0
  ],
  "fragmentation": [
    {
      "category": 0,
      "components": 1,
      "largestArea": 92124,
      "secondaryComponents": 0,
      "smallComponents": 0,
      "smallArea": 0,
      "enclaveCandidates": 0,
      "topComponents": [
        {
          "area": 92124,
          "bounds": [
            -349,
            1685,
            88,
            1982
          ],
          "seed": [
            -137,
            1685
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [
            2
          ],
          "enclaveCandidate": false
        }
      ],
      "smallExamples": [],
      "enclaveExamples": []
    },
    {
      "category": 1,
      "components": 0,
      "largestArea": 0,
      "secondaryComponents": 0,
      "smallComponents": 0,
      "smallArea": 0,
      "enclaveCandidates": 0,
      "topComponents": [],
      "smallExamples": [],
      "enclaveExamples": []
    },
    {
      "category": 2,
      "components": 1,
      "largestArea": 13661,
      "secondaryComponents": 0,
      "smallComponents": 0,
      "smallArea": 0,
      "enclaveCandidates": 0,
      "topComponents": [
        {
          "area": 13661,
          "bounds": [
            89,
            1664,
            240,
            1841
          ],
          "seed": [
            224,
            1664
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [
            0,
            4
          ],
          "enclaveCandidate": false
        }
      ],
      "smallExamples": [],
      "enclaveExamples": []
    },
    {
      "category": 3,
      "components": 0,
      "largestArea": 0,
      "secondaryComponents": 0,
      "smallComponents": 0,
      "smallArea": 0,
      "enclaveCandidates": 0,
      "topComponents": [],
      "smallExamples": [],
      "enclaveExamples": []
    },
    {
      "category": 4,
      "components": 2102,
      "largestArea": 1568588,
      "secondaryComponents": 2101,
      "smallComponents": 2097,
      "smallArea": 6479,
      "enclaveCandidates": 0,
      "topComponents": [
        {
          "area": 1568588,
          "bounds": [
            227,
            1453,
            2091,
            3214
          ],
          "seed": [
            507,
            1453
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [
            2
          ],
          "enclaveCandidate": false
        },
        {
          "area": 575363,
          "bounds": [
            -718,
            1419,
            280,
            2518
          ],
          "seed": [
            -108,
            1419
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 324,
          "bounds": [
            1808,
            3068,
            1837,
            3086
          ],
          "seed": [
            1828,
            3068
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 74,
          "bounds": [
            611,
            2373,
            622,
            2390
          ],
          "seed": [
            616,
            2373
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 68,
          "bounds": [
            741,
            2411,
            756,
            2423
          ],
          "seed": [
            753,
            2411
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 63,
          "bounds": [
            1782,
            3060,
            1790,
            3073
          ],
          "seed": [
            1783,
            3060
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 58,
          "bounds": [
            1018,
            1927,
            1026,
            1941
          ],
          "seed": [
            1022,
            1927
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 56,
          "bounds": [
            805,
            2400,
            822,
            2408
          ],
          "seed": [
            817,
            2400
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 54,
          "bounds": [
            1022,
            1998,
            1033,
            2009
          ],
          "seed": [
            1029,
            1998
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 54,
          "bounds": [
            655,
            2430,
            668,
            2444
          ],
          "seed": [
            667,
            2430
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 45,
          "bounds": [
            1032,
            1864,
            1041,
            1876
          ],
          "seed": [
            1038,
            1864
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 45,
          "bounds": [
            626,
            2375,
            635,
            2386
          ],
          "seed": [
            635,
            2375
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 42,
          "bounds": [
            1044,
            1862,
            1056,
            1869
          ],
          "seed": [
            1047,
            1862
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 41,
          "bounds": [
            725,
            2425,
            737,
            2435
          ],
          "seed": [
            734,
            2425
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 39,
          "bounds": [
            1019,
            1968,
            1029,
            1976
          ],
          "seed": [
            1022,
            1968
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 39,
          "bounds": [
            1497,
            2399,
            1506,
            2409
          ],
          "seed": [
            1497,
            2399
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 39,
          "bounds": [
            961,
            2800,
            969,
            2813
          ],
          "seed": [
            964,
            2800
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 34,
          "bounds": [
            824,
            2405,
            830,
            2415
          ],
          "seed": [
            829,
            2405
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 33,
          "bounds": [
            784,
            2403,
            794,
            2411
          ],
          "seed": [
            788,
            2403
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 31,
          "bounds": [
            1013,
            1959,
            1020,
            1968
          ],
          "seed": [
            1017,
            1959
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        }
      ],
      "smallExamples": [
        {
          "area": 63,
          "bounds": [
            1782,
            3060,
            1790,
            3073
          ],
          "seed": [
            1783,
            3060
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 58,
          "bounds": [
            1018,
            1927,
            1026,
            1941
          ],
          "seed": [
            1022,
            1927
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 56,
          "bounds": [
            805,
            2400,
            822,
            2408
          ],
          "seed": [
            817,
            2400
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 54,
          "bounds": [
            1022,
            1998,
            1033,
            2009
          ],
          "seed": [
            1029,
            1998
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 54,
          "bounds": [
            655,
            2430,
            668,
            2444
          ],
          "seed": [
            667,
            2430
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 45,
          "bounds": [
            1032,
            1864,
            1041,
            1876
          ],
          "seed": [
            1038,
            1864
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 45,
          "bounds": [
            626,
            2375,
            635,
            2386
          ],
          "seed": [
            635,
            2375
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 42,
          "bounds": [
            1044,
            1862,
            1056,
            1869
          ],
          "seed": [
            1047,
            1862
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 41,
          "bounds": [
            725,
            2425,
            737,
            2435
          ],
          "seed": [
            734,
            2425
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 39,
          "bounds": [
            1019,
            1968,
            1029,
            1976
          ],
          "seed": [
            1022,
            1968
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 39,
          "bounds": [
            1497,
            2399,
            1506,
            2409
          ],
          "seed": [
            1497,
            2399
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 39,
          "bounds": [
            961,
            2800,
            969,
            2813
          ],
          "seed": [
            964,
            2800
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 34,
          "bounds": [
            824,
            2405,
            830,
            2415
          ],
          "seed": [
            829,
            2405
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 33,
          "bounds": [
            784,
            2403,
            794,
            2411
          ],
          "seed": [
            788,
            2403
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 31,
          "bounds": [
            1013,
            1959,
            1020,
            1968
          ],
          "seed": [
            1017,
            1959
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 31,
          "bounds": [
            714,
            2429,
            724,
            2437
          ],
          "seed": [
            723,
            2429
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 30,
          "bounds": [
            855,
            2392,
            866,
            2396
          ],
          "seed": [
            856,
            2392
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 28,
          "bounds": [
            593,
            2408,
            601,
            2414
          ],
          "seed": [
            595,
            2408
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 28,
          "bounds": [
            599,
            2416,
            608,
            2422
          ],
          "seed": [
            607,
            2416
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        },
        {
          "area": 27,
          "bounds": [
            918,
            2462,
            924,
            2469
          ],
          "seed": [
            923,
            2462
          ],
          "touchesWater": true,
          "touchesStudyEdge": false,
          "neighbors": [],
          "enclaveCandidate": false
        }
      ],
      "enclaveExamples": []
    },
    {
      "category": 5,
      "components": 0,
      "largestArea": 0,
      "secondaryComponents": 0,
      "smallComponents": 0,
      "smallArea": 0,
      "enclaveCandidates": 0,
      "topComponents": [],
      "smallExamples": [],
      "enclaveExamples": []
    }
  ],
  "threshold": 64,
  "method": "4-neighbor; adjacency counts shared unit land edges; water crossings excluded. Enclave candidate: no water/study edge and exactly one surrounding other class. Fragment: area<threshold; disconnected areas may be natural islands. UNASSIGNED/DISPUTED are explicit classes, not errors repaired automatically."
}
```
